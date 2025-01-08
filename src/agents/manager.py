from typing import Dict, Any, List
from .base import BaseAgent
from .messages import Message, TaskType

class ManagerAgent(BaseAgent):
    """Main orchestrator agent that coordinates all operations"""
    
    def __init__(self):
        super().__init__('manager_1', 'manager')
        self.specialized_agents = {}
        self.active_tasks = {}
    
    async def register_agent(self, agent: BaseAgent):
        """Register a new specialized agent"""
        self.specialized_agents[agent.agent_id] = agent
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming messages and delegate to appropriate agent"""
        message_type = message.get('type')
        if message_type == 'task_request':
            return await self.delegate_task(message)
        elif message_type == 'status_update':
            return await self.update_task_status(message)
        return {'status': 'error', 'message': 'Unknown message type'}
    
    async def delegate_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate tasks to appropriate specialized agents"""
        task_type = task.get('task_type')
        if task_type in TaskType.ML_TASKS:
            agent = self.specialized_agents.get('tensorflow_1')
            if agent:
                return await agent.handle_task(task)
        return {'status': 'error', 'message': 'No suitable agent found'}
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle high-level task coordination"""
        task_id = task.get('task_id')
        self.active_tasks[task_id] = task
        result = await self.delegate_task(task)
        return result