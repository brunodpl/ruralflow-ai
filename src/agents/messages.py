from enum import Enum
from typing import Dict, Any
from dataclasses import dataclass

class TaskType(Enum):
    """Enumeration of supported task types"""
    PRICE_PREDICTION = 'price_prediction'
    MARKET_MATCHING = 'market_matching'
    RECOMMENDATION = 'recommendation'
    
    @classmethod
    @property
    def ML_TASKS(cls) -> set:
        """Set of all ML-related tasks"""
        return {cls.PRICE_PREDICTION, cls.MARKET_MATCHING, cls.RECOMMENDATION}

@dataclass
class Message:
    """Base message structure for agent communication"""
    message_id: str
    type: str
    sender: str
    receiver: str
    content: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary format"""
        return {
            'message_id': self.message_id,
            'type': self.type,
            'sender': self.sender,
            'receiver': self.receiver,
            'content': self.content
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create message from dictionary"""
        return cls(
            message_id=data['message_id'],
            type=data['type'],
            sender=data['sender'],
            receiver=data['receiver'],
            content=data['content']
        )