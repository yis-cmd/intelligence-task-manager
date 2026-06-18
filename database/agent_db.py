from database.base_repository import BaseRepository
from database.base_models import Agent, AgentCreate, AgentUpdate

class AgentNotExistsError(KeyError):
    pass

class AgentDB(BaseRepository):
    def __init__(self) -> None:
        super().__init__()
        self.table_name = "agents"
        self.connection_pool.create_database()
        self.connection_pool.create_tables()

    def create_agent(self, data: AgentCreate):
        self.insert(self.table_name, data.model_dump())
        response = self.select(self.table_name, data.model_dump())
        if len(response) > 1:
            return response[len(response) -1]
        return response[0]

    def get_all_agents(self):
        return self.select(self.table_name)

    def get_agent_by_id(self, id):
        response =  self.select(self.table_name, {"id": id})
        if not response:
            raise AgentNotExistsError
        return Agent.model_validate(response[0])

    def update_agent(self, id, data: AgentUpdate):
        self.update(self.table_name, data, {"id": id})
        return True

    def deactivate_agent(self, id):
        self.update(self.table_name, AgentUpdate.model_validate({"is_active": False}), {"id": id})
        return True

    def increment_completed(self, id: int):
        self._execute(f"UPDATE `agents` SET completed_missions = completed_missions + 1 WHERE id = {id}")
        return True

    def increment_failed(self, id):
        self._execute(f"UPDATE `agents` SET failed_missions = failed_missions + 1 WHERE id = {id}")
        return True

    def get_agent_performance(self, id):
        agent = self.get_agent_by_id(id)
        assigned: int = len(
            self.select("missions", {"assigned_agent_id": id, "status": "ASSIGNED"})
        )
        in_progress: int = len(
            self.select("missions", {"assigned_agent_id": id, "status": "IN_PROGRESS"})
        )
        total = agent.failed_missions + agent.completed_missions + assigned + in_progress
        if total == 0:
            return {
                "failed": "not enough missions to check"
            }
        return {
            "completed": agent.completed_missions,
            "failed": agent.failed_missions,
            "total": total,
            "success rate": agent.completed_missions / total * 100,
        }

    def count_active_agents(self):
        return self.count(self.table_name, {"is_active": True})
