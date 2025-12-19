"""
Amorce-wrapped CrewAI tools with signatures + HITL
"""

from typing import Optional, Any


class AmorceToolWrapper:
    """
    Wraps CrewAI tool with Amorce security.
    
    Adds:
    - Ed25519 signatures to tool calls
    - HITL approvals for sensitive operations
    - Transaction logging
    """
    
    def __init__(
        self,
        tool: Any,
        identity: Any,
        client: Any,
        requires_hitl: bool = False
    ):
        """
        Initialize tool wrapper.
        
        Args:
            tool: Original CrewAI tool
            identity: Amorce IdentityManager
            client: Amorce client
            requires_hitl: Whether this tool requires human approval
        """
        self.tool = tool
        self.name = getattr(tool, 'name', tool.__class__.__name__)
        self.description = getattr(tool, 'description', '')
        self.identity = identity
        self.client = client
        self.requires_hitl = requires_hitl
    
    def run(self, *args, **kwargs) -> Any:
        """
        Run tool with Amorce signature.
        
        Returns tool result with security metadata.
        """
        import json
        
        # Prepare tool call data
        call_data = {
            'tool': self.name,
            'args': list(args),
            'kwargs': kwargs,
            'agent_id': self.identity.agent_id
        }
        
        # Sign the tool call
        signature = self.identity.sign(json.dumps(call_data, sort_keys=True))
        
        # HITL if required
        if self.requires_hitl:
            print(f"\n⏸️  HUMAN APPROVAL REQUIRED for {self.name}")
            print(f"   Tool: {self.name}")
            print(f"   Agent: {self.identity.agent_id}")
            
            approval_id = self.client.request_approval(
                summary=f"Approve {self.name} execution",
                details=call_data,
                timeout_seconds=300
            )
            
            # Wait for approval
            import time
            max_wait = 300
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                status = self.client.check_approval(approval_id)
                
                if status['status'] == 'approved':
                    print(f"✅ Approval granted for {self.name}")
                    break
                elif status['status'] in ['rejected', 'expired']:
                    raise PermissionError(f"HITL approval denied for {self.name}")
                
                time.sleep(1)
            else:
                raise TimeoutError(f"HITL approval timeout for {self.name}")
        
        # Execute original tool
        if hasattr(self.tool, 'run'):
            result = self.tool.run(*args, **kwargs)
        elif callable(self.tool):
            result = self.tool(*args, **kwargs)
        else:
            raise TypeError(f"Tool {self.name} is not callable")
        
        # Return with signature proof
        return {
            'result': result,
            'tool': self.name,
            'agent_id': self.identity.agent_id,
            'signature': signature
        }
    
    def __call__(self, *args, **kwargs):
        """Make wrapper callable."""
        return self.run(*args, **kwargs)
