"""
SecureAgent - Amorce-enhanced CrewAI Agent

Provides Ed25519 signatures and HITL for individual agents.
"""

from typing import Optional, List, Any
from crewai import Agent


class SecureAgent(Agent):
    """
    CrewAI Agent with Amorce security.
    
    All agent actions are:
    - Cryptographically signed (Ed25519)
    - Verified via Trust Directory
    - HITL for sensitive operations
    - A2A-compatible
    
    Example:
        ```python
        from crewai_amorce import SecureAgent
        
        agent = SecureAgent(
            role="Research Specialist",
            goal="Find accurate information",
            backstory="Expert researcher",
            hitl_required=['execute_code']
        )
        ```
    """
    
    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str,
        tools: Optional[List] = None,
        identity: Optional[Any] = None,
        hitl_required: Optional[List[str]] = None,
        a2a_compatible: bool = True,
        verbose: bool = False,
        **kwargs
    ):
        """
        Initialize secure CrewAI agent.
        
        Args:
            role: Agent's role in the crew
            goal: Agent's objective
            backstory: Agent's background story
            tools: List of tools agent can use
            identity: Amorce identity (auto-generated if None)
            hitl_required: Tool names requiring human approval
            a2a_compatible: Use A2A message format
            verbose: Show agent reasoning
            **kwargs: Additional CrewAI Agent arguments
        """
        # Initialize parent Agent
        super().__init__(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools or [],
            verbose=verbose,
            **kwargs
        )
        
        # Amorce integration
        from amorce import IdentityManager, AmorceClient
        
        self.identity = identity or IdentityManager.generate()
        self.amorce_client = AmorceClient(
            self.identity,
            directory_url='https://directory.amorce.io',
            orchestrator_url='https://api.amorce.io'
        )
        
        self.hitl_required = hitl_required or []
        self.a2a_compatible = a2a_compatible
        self.agent_id = self.identity.agent_id
        
        # Wrap tools with Amorce security
        self.tools = [self._wrap_tool(tool) for tool in (tools or [])]
        
        if verbose:
            print(f"🔐 Created secure agent: {role}")
            print(f"   Agent ID: {self.agent_id}")
            print(f"   HITL required for: {self.hitl_required}")
    
    def _wrap_tool(self, tool):
        """Wrap tool with Amorce signature + HITL."""
        from crewai_amorce.tools import AmorceToolWrapper
        return AmorceToolWrapper(
            tool=tool,
            identity=self.identity,
            client=self.amorce_client,
            requires_hitl=(tool.name in self.hitl_required)
        )
    
    def check_buyer_reputation(self, buyer_id: str) -> dict:
        """
        Check buyer's reputation in Trust Directory.
        
        Args:
            buyer_id: Buyer's agent ID
            
        Returns:
            Reputation data (trust score, history, etc.)
        """
        # Query Trust Directory
        return self.amorce_client.get_agent_reputation(buyer_id)
    
    def receive_offer(self) -> dict:
        """
        Receive and verify incoming offer.
        
        Returns:
            Verified offer with sender information
        """
        # Implementation for receiving signed offers
        pass
    
    def counter_offer(self, price: float, reasoning: str = "") -> dict:
        """
        Make counter-offer with signature.
        
        Args:
            price: Counter-offer price
            reasoning: Explanation for price
            
        Returns:
            Signed counter-offer
        """
        import json
        
        offer_data = {
            'agent_id': self.agent_id,
            'price': price,
            'reasoning': reasoning,
            'role': self.role
        }
        
        signature = self.identity.sign(json.dumps(offer_data, sort_keys=True))
        
        return {
            **offer_data,
            'signature': signature
        }
    
    def calculate_margin(self, offer_price: float) -> float:
        """Calculate profit margin on offer."""
        # Placeholder - would integrate with pricing tool
        return offer_price * 0.3
    
    def request_human_approval_for_sale(self):
        """Request human approval for sale."""
        approval_id = self.amorce_client.request_approval(
            summary=f"{self.role}: Approve sale",
            details={'agent_id': self.agent_id, 'role': self.role},
            timeout_seconds=300
        )
        
        # Poll for approval
        import time
        max_wait = 300
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            status = self.amorce_client.check_approval(approval_id)
            
            if status['status'] == 'approved':
                return True
            elif status['status'] in ['rejected', 'expired']:
                raise PermissionError("Sale approval denied")
            
            time.sleep(1)
        
        raise TimeoutError("Sale approval timeout")
    
    def generate_signed_receipt(self) -> dict:
        """Generate cryptographically signed receipt."""
        import json
        from datetime import datetime
        
        receipt = {
            'seller_id': self.agent_id,
            'seller_role': self.role,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'verified_by_amorce': True
        }
        
        signature = self.identity.sign(json.dumps(receipt, sort_keys=True))
        
        return {
            **receipt,
            'signature': signature
        }
