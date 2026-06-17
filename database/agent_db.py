from base_repository import BaseRepository
from database.base_models import AgentCreate, AgentUpdate
class Agents(BaseRepository):
    def __init__(self) -> None:
        super().__init__()
        self.table_name = "agents"

    def create_agent(self, data:AgentCreate):
        self.insert(self.table_name, data.model_dump())
        return self.select(self.table_name, data.model_dump())
    
    def get_all_agents(self):
        return self.select(self.table_name)
    
    def get_agent_by_id(self, id):
        return self.select(self.table_name, {"id":id})
    
    def update_agent(self, id, data:AgentUpdate):
        self.update(self.table_name, data.model_dump(), {"id":id})
        return True

    def deactivate_agent(self, id):
        self.update(self.table_name, {"is_active": False}, {"id":id})
        return True
        
    def increment_completed(self, id:int):
        self._execute(f"UPDATE `agents` SET completed = completed + 1 WHERE id = {id}")
        return True
    
    def increment_failed(self, id):
        self._execute(f"UPDATE `agents` SET failed = failed + 1 WHERE id = {id}")
        return True
    
    def get_agent_performance(self, id):# returns dict with the keys (completed, failed, total, success rate)
        agent = self.select(self.table_name, {"id":id})[0]
        total = agent.failed_missions + agent.completed_missions
        return {
            "completed":agent.completed_missions,
            "failed":agent.failed_missions,
            "total": total,
            "success rate": agent.completed_missions / total * 100
        }
    
    def count_active_agents(self):
        return len(self.count(self.table_name, {"is_active":True}))