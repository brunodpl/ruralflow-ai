from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.status = 'idle'
    
    @abstractmethod
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming messages"""
        pass
    
    @abstractmethod
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle specific tasks"""
        pass
    
    def get_status(self) -> Dict[str, str]:
        """Get current agent status"""
        return {
            'agent_id': self.agent_id,
            'type': self.agent_type,
            'status': self.status
        }