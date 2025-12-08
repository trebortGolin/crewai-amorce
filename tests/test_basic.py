"""
Basic tests for crewai-amorce
"""

import pytest
from unittest.mock import Mock, MagicMock

def test_secure_crew_decorator():
    """Test that @secure_crew decorator works."""
    from crewai_amorce import secure_crew
    from crewai import Crew, Agent, Task
    
    # Create mock crew
    agent = Agent(
        role="Test Agent",
        goal="Test",
        backstory="Test"
    )
    
    task = Task(description="Test task", agent=agent)
    
    try:
        @secure_crew
        crew = Crew(agents=[agent], tasks=[task])
        
        assert hasattr(crew, 'crew_id')
        assert hasattr(crew, 'amorce_identity')
        assert hasattr(crew, 'discover_crews')
    except ImportError:
        pytest.skip("Amorce SDK not available")

def test_secure_agent_creation():
    """Test SecureAgent initialization."""
    from crewai_amorce import SecureAgent
    
    try:
        agent = SecureAgent(
            role="Test Agent",
            goal="Test tasks",
            backstory="Test agent",
            hitl_required=['dangerous_action']
        )
        
        assert agent.role == "Test Agent"
        assert agent.agent_id is not None
        assert 'dangerous_action' in agent.hitl_required
    except ImportError:
        pytest.skip("Amorce SDK not available")

def test_counter_offer():
    """Test counter-offer generation."""
    from crewai_amorce import SecureAgent
    
    try:
        agent = SecureAgent(
            role="Seller",
            goal="Sell products",
            backstory="Professional seller"
        )
        
        counter = agent.counter_offer(price=500, reasoning="Fair price")
        
        assert counter['price'] == 500
        assert counter['reasoning'] == "Fair price"
        assert 'signature' in counter
        assert counter['agent_id'] == agent.agent_id
    except ImportError:
        pytest.skip("Amorce SDK not available")

def test_a2a_envelope():
    """Test A2AEnvelope for CrewAI."""
    from crewai_amorce.a2a import A2AEnvelope
    
    envelope = A2AEnvelope(
        sender_id="test_crew",
        message="Test message",
        signature="fake_sig"
    )
    
    data = envelope.to_dict()
    
    assert data['protocol'] == 'a2a/1.0'
    assert data['security']['sender_id'] == 'test_crew'
    assert data['payload']['message'] == 'Test message'

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
