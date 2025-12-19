"""
@secure_crew decorator for CrewAI

Wraps entire crews with Amorce security.
"""

from typing import Optional, List, Any
from functools import wraps


def secure_crew(
    crew_class=None,
    *,
    identity: Optional[Any] = None,
    hitl_required: Optional[List[str]] = None,
    a2a_compatible: bool = True,
    verbose: bool = False
):
    """
    Decorator to secure an entire CrewAI crew.
    
    Usage:
        ```python
        @secure_crew
        crew = Crew(agents=[...], tasks=[...])
        
        # Or with options:
        @secure_crew(hitl_required=['execute_code'])
        crew = Crew(agents=[...], tasks=[...])
        ```
    
    Args:
        crew_class: Crew instance (auto-provided by decorator)
        identity: Amorce identity (auto-generated if None)
        hitl_required: Action names requiring human approval
        a2a_compatible: Use A2A message format
        verbose: Show security logs
    
    Returns:
        Secured crew with Amorce integration
    """
    
    def decorator(crew):
        """Actual decorator function."""
        from amorce import IdentityManager, AmorceClient
        
        # Generate or load identity
        crew_identity = identity or IdentityManager.generate()
        
        # Initialize Amorce client
        amorce_client = AmorceClient(
            crew_identity,
            directory_url='https://directory.amorce.io',
            orchestrator_url='https://api.amorce.io'
        )
        
        # Add Amorce metadata to crew
        crew.amorce_identity = crew_identity
        crew.amorce_client = amorce_client
        crew.hitl_required = hitl_required or []
        crew.a2a_compatible = a2a_compatible
        crew.crew_id = crew_identity.agent_id
        
        if verbose:
            print(f"🔐 Secured crew with ID: {crew.crew_id}")
        
        # Wrap crew methods
        original_kickoff = crew.kickoff
        
        def secure_kickoff(*args, **kwargs):
            """Secured kickoff method."""
            if verbose:
                print(f"🚀 Starting secure crew {crew.crew_id}")
                print(f"   Agents: {len(crew.agents)}")
                print(f"   Tasks: {len(crew.tasks)}")
                print(f"   HITL required for: {crew.hitl_required}")
            
            # Sign the kickoff
            import json
            kickoff_data = {
                'crew_id': crew.crew_id,
                'agents': [agent.role for agent in crew.agents],
                'tasks': [task.description[:50] for task in crew.tasks]
            }
            signature = crew_identity.sign(json.dumps(kickoff_data, sort_keys=True))
            
            if verbose:
                print(f"   Kickoff signature: {signature[:50]}...")
            
            # Execute original kickoff
            result = original_kickoff(*args, **kwargs)
            
            # Return with security metadata
            if a2a_compatible:
                from crewai_amorce.a2a import A2AEnvelope
                return {
                    'result': result,
                    'crew_id': crew.crew_id,
                    'signature': signature,
                    'protocol': 'a2a/1.0',
                    'security_layer': 'amorce/3.0'
                }
            
            return result
        
        # Replace methods
        crew.kickoff = secure_kickoff
        
        # Add helper methods
        def discover_crews(capability: str):
            """Discover other crews in Trust Directory."""
            return amorce_client.discover(capability)
        
        def delegate_to(target_crew, task: str):
            """Delegate task to another crew."""
            # Implementation for inter-crew delegation
            pass
        
        crew.discover_crews = discover_crews
        crew.delegate_to = delegate_to
        
        return crew
    
    # Handle @secure_crew vs @secure_crew()
    if crew_class is None:
        # Called with arguments: @secure_crew(hitl_required=[...])
        return decorator
    else:
        # Called without arguments: @secure_crew
        return decorator(crew_class)
