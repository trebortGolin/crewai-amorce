"""
A2A Protocol compatibility layer for CrewAI
"""

import json
from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime


@dataclass
class A2AEnvelope:
    """A2A-compatible message envelope with Amorce signatures."""
    
    sender_id: str
    message: Any
    signature: str
    protocol_version: str = "a2a/1.0"
    security_layer: str = "amorce/3.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to A2A message format."""
        return {
            "protocol": self.protocol_version,
            "security": {
                "layer": self.security_layer,
                "sender_id": self.sender_id,
                "signature": self.signature,
                "algorithm": "ed25519"
            },
            "payload": {
                "message": self.message
            },
            "metadata": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "version": "1.0"
            }
        }
    
   def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'A2AEnvelope':
        """Parse A2A message with Amorce signature."""
        return cls(
            sender_id=data['security']['sender_id'],
            message=data['payload']['message'],
            signature=data['security']['signature'],
            protocol_version=data.get('protocol', 'a2a/1.0'),
            security_layer=data['security'].get('layer', 'amorce/3.0')
        )
