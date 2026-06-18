from database.base_models import Agent, Mission, MissionCreate, MissionRiskLevel, MissionUpdate, MissionStatus, RiskLevel
from database.base_repository import BaseRepository

class MissionNotExistsError(KeyError):
    pass


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
        mission = MissionRiskLevel.model_validate(dict(data.model_dump() | {"risk_level":risk_level}))
        self.insert(self.table_name, mission.model_dump())
        response = self.select(self.table_name, mission.model_dump())
        if len(response) > 1:
            return response[len(response) -1]
        return response[0]

    def get_all_missions(self):
        return self.select(self.table_name)

    def get_mission_by_id(self, id):
        response =  self.select(self.table_name, {"id": id})
        if not response:
            raise MissionNotExistsError
        return Mission.model_validate(response[0])

    def assign_mission(self, m_id, a_id):
        self.update(self.table_name, MissionUpdate.model_validate({"assigned_agent_id":a_id}), {"id":m_id})
        return True
        

    def update_mission_status(
        self, id, status
    ):  
        self.update(self.table_name, MissionUpdate.model_validate({"status":status}), {"id":id})
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
        return self.count(self.table_name, {"status": status})

    def count_open_missions(self):
        assigned = self.select(self.table_name, {"status": "ASSIGNED"})
        in_progress = self.select(self.table_name, {"status": "IN_PROGRESS"})
        return assigned + in_progress

    def count_critical_missions(self):
        return self.select(self.table_name, {"risk_level": "CRITICAL"})
