from database.base_models import Agent, Mission, MissionCreate, MissionUpdate, MissionStatus, RiskLevel
from database.base_repository import BaseRepository


def calculate_risk_level(difficulty: int, importance: int):
    value = difficulty * 2 + importance
    if 1 <= value <= 9:
        return "LOW"
    elif 10 <= value <= 17:
        return "MEDIUM"
    elif 18 <= value <= 24:
        return "HIGH"
    elif 25 <= value:
        return "CRITICAL"


class MissionDB(BaseRepository):
    def __init__(self) -> None:
        super().__init__()
        self.table_name = "missions"

    def create_mission(self, data: MissionCreate):
        risk_level = (RiskLevel(calculate_risk_level(data.difficulty, data.importance)))
        mission = Mission.model_validate(data.model_dump() | {risk_level:risk_level})
        self.insert(self.table_name, mission.model_dump())
        return self.select(self.table_name, mission.model_dump())

    def get_all_missions(self):
        return self.select(self.table_name)

    def get_mission_by_id(self, id):
        return self.select(self.table_name, {"id": id})

    def assign_mission(self, m_id, a_id):
        agent = self.select("agents", {"id":a_id})
        mission = self.select(self.table_name, {"id":m_id})
        if not agent or not mission:
            raise ValueError
        agent = Agent.model_validate(agent[0])
        mission = Mission.model_validate(mission[0])
        if mission.risk_level == "CRITICAL" and agent.agent_rank != "Commander":
            return False
        if mission.status != "NEW":
            return False
        self.update(self.table_name, {"assigned_agent_id":a_id})
        return True
        

    def update_mission_status(
        self, id, status
    ):  
        mission = Mission.model_validate(self.select(self.table_name, {"id":id})[0])
        if status == "CANCELLED":
            pass
        elif status == "NEW":
            raise ValueError
        elif status == "ASSIGNED" and mission.status != "NEW":
            return False
        elif status == "IN_PROGRESS" and mission.status != "ASSIGNED":
            return False
        elif status == ("FAILED" or "COMPLETED") and mission.status != "IN_PROGRESS":
            return False
        self.update(self.table_name, {"status":status})
        return True

    def get_open_missions_by_agent(self, id):
        assigned = self.select(
            self.table_name, {"assigned_agent_id": id, "status": "ASSIGNED"}
        )
        in_progress = self.select(
            self.table_name, {"assigned_agent_id": id, "status": "IN_PROGRESS"}
        )
        return assigned + in_progress

    def count_all_missions(self):
        return self.count(self.table_name)

    def count_by_status(self, status):
        try:
            MissionStatus(status)
        except Exception:
            raise ValueError("Invalid status")
        return self.count(self.table_name, {"status": status})

    def count_open_missions(self):
        assigned = self.select(self.table_name, {"status": "ASSIGNED"})
        in_progress = self.select(self.table_name, {"status": "IN_PROGRESS"})
        return assigned + in_progress

    def count_critical_missions(self):
        return self.select(self.table_name, {"risk_level": "CRITICAL"})
