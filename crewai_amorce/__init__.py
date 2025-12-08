"""
CrewAI-Amorce Integration

Secure CrewAI crews with Ed25519 signatures and HITL approvals.
"""

from crewai_amorce.decorators import secure_crew
from crewai_amorce.agent import SecureAgent

__version__ = "0.1.0"
__all__ = ["secure_crew", "SecureAgent"]
