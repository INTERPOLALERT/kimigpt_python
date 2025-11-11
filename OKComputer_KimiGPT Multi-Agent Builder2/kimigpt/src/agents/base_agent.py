from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
import logging
from datetime import datetime

class BaseAgent(ABC):
    def __init__(self, name: str, agent_id: str):
        self.name = name
        self.agent_id = agent_id
        self.status = "idle"
        self.last_activity = None
        self.context = {}
        self.logger = logging.getLogger(f"agent.{agent_id}")
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results"""
        pass
    
    def update_status(self, status: str):
        """Update agent status"""
        self.status = status
        self.last_activity = datetime.now()
        self.logger.info(f"Status updated to: {status}")
    
    def set_context(self, key: str, value: Any):
        """Set context data for the agent"""
        self.context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context data"""
        return self.context.get(key, default)
    
    def log_activity(self, message: str, level: str = "info"):
        """Log agent activity"""
        getattr(self.logger, level)(message)
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data"""
        return True  # Override in subclasses
    
    async def cleanup(self):
        """Cleanup resources"""
        self.update_status("idle")