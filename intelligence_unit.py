from pydantic import ValidationError

from database.base_models import Agent, Mission, MissionStatus, MissionUpdate
from database.mission_db import MissionDB, MissionNotExistsError
from database.agent_db import AgentDB, AgentNotExistsError

agent_manager = AgentDB()
mission_manager = MissionDB()

class MissionAlreadyAssignedError(KeyError):
    pass

class AgentInactiveError(Exception):
    pass

class AgentNotAuthorizedError(Exception):
    pass

class TooManyMissionsError(Exception):
    pass

class OngoingMissionCancellingError(Exception):
    pass

class InvalidUpdateStatusError(Exception):
    pass

def assign_mission(m_id: int, a_id: int):
    agent = agent_manager.get_agent_by_id(a_id)
    mission = mission_manager.get_mission_by_id(m_id)
    if len(mission_manager.get_open_missions_by_agent(a_id)) > 3:
        raise TooManyMissionsError
    if mission.status != "NEW":
        raise MissionAlreadyAssignedError
    if not agent.is_active:
        raise AgentInactiveError
    if mission.risk_level == "CRITICAL" and agent.agent_rank != "Commander":
        raise AgentNotAuthorizedError
    mission_manager.assign_mission(m_id, a_id)
    mission_manager.update_mission_status(
        m_id, MissionUpdate(status=MissionStatus.ASSIGNED)
    )

def update_mission_status(m_id, status:MissionStatus):
    mission = mission_manager.get_mission_by_id(m_id)
    if status == "CANCELLED" and mission.status != ("NEW" or "ASSIGNED"):
        raise OngoingMissionCancellingError
    elif status == "NEW":
        raise InvalidUpdateStatusError("cannot update to NEW")
    elif status == "ASSIGNED" and mission.status != "NEW":
        raise InvalidUpdateStatusError("can only assign a new mission")
    elif status == "IN_PROGRESS" and mission.status != "ASSIGNED":
        raise InvalidUpdateStatusError("can only start assigned missions")
    elif status == ("FAILED" or "COMPLETED") and mission.status != "IN_PROGRESS":
        raise InvalidUpdateStatusError("not ongoing mission cannot be completed")
    mission_manager.update_mission_status(m_id, status)
    return True

def complete_mission(m_id):
    mission = mission_manager.get_mission_by_id(m_id)
    update_mission_status(m_id, MissionStatus.COMPLETED)
    assert mission.assigned_agent_id
    agent_manager.increment_completed(mission.assigned_agent_id)

def cancel_mission(m_id:int):
    update_mission_status(m_id, MissionStatus.CANCELLED)

def failed_mission(m_id):
    mission = mission_manager.get_mission_by_id(m_id)
    update_mission_status(m_id, MissionStatus.FAILED)
    assert mission.assigned_agent_id
    agent_manager.increment_failed(mission.assigned_agent_id)

def deactivate_agent(a_id:int):
    agent = agent_manager.get_agent_by_id(a_id)
    if not agent.is_active:
        raise AgentInactiveError
    agent_manager.deactivate_agent(a_id)