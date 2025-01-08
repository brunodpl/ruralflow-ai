from typing import Dict, Any
from dataclasses import dataclass
from uuid import uuid4

@dataclass
class Task:
    """Base task structure"""
    task_id: str
    task_type: str
    data: Dict[str, Any]
    priority: int = 1
    status: str = 'pending'
    
    @classmethod
    def create(cls, task_type: str, data: Dict[str, Any], priority: int = 1) -> 'Task':
        """Create a new task with generated ID"""
        return cls(
            task_id=str(uuid4()),
            task_type=task_type,
            data=data,
            priority=priority
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary format"""
        return {
            'task_id': self.task_id,
            'task_type': self.task_type,
            'data': self.data,
            'priority': self.priority,
            'status': self.status
        }