from pydantic import ValidationError

from database.base_models import Agent, Mission, MissionStatus, MissionUpdate
from database.mission_db import MissionDB
from database.agent_db import AgentDB

agent_manager = AgentDB()
mission_manager = MissionDB()


def assign_mission(m_id: int, a_id: int):
    try:
        agent = Agent.model_validate(agent_manager.get_agent_by_id(a_id)[0])
        mission = Mission.model_validate(mission_manager.get_mission_by_id(m_id)[0])
    except ValidationError:
        raise
    agent_mission_count = len(mission_manager.get_open_missions_by_agent(a_id))
    if mission.status != "NEW":
        return False
    if not agent.is_active:
        return False
    if mission.risk_level == "CRITICAL" and agent.agent_rank != "Commander":
        return False
    if agent_mission_count >= 3:
        return False
    mission_manager.assign_mission(m_id, a_id)
    mission_manager.update_mission_status(
        m_id, MissionUpdate(status=MissionStatus.ASSIGNED)
    )

def update_mission_status(m_id, status:MissionStatus):
    try:
        mission = Mission.model_validate(mission_manager.get_mission_by_id(m_id)[0])
    except Exception:
        raise ValueError
    if status == "CANCELLED" and mission.status != ("NEW" or "ASSIGNED"):
        raise ValueError
    elif status == "NEW":
        raise ValueError
    elif status == "ASSIGNED" and mission.status != "NEW":
        raise ValueError
    elif status == "IN_PROGRESS" and mission.status != "ASSIGNED":
        raise ValueError
    elif status == ("FAILED" or "COMPLETED") and mission.status != "IN_PROGRESS":
        raise ValueError
    mission_manager.update_mission_status(m_id, status)
    return True

def complete_mission(m_id):
    try:
        mission = Mission.model_validate(mission_manager.get_mission_by_id(m_id)[0])
    except Exception:
        raise ValueError
    if mission.status != "IN_PROGRESS":
        raise ValueError
    update_mission_status(m_id, MissionStatus.COMPLETED)
    assert mission.assigned_agent_id
    agent_manager.increment_completed(mission.assigned_agent_id)

def cancel_mission(m_id:int):
    try:
        mission = Mission.model_validate(mission_manager.get_mission_by_id(m_id)[0])
    except Exception:
        raise ValueError
    if mission.status != ("NEW" or "ASSIGNED"):
        raise ValueError
    update_mission_status(m_id, MissionStatus.CANCELLED)

def failed_mission(m_id):
    try:
        mission = Mission.model_validate(mission_manager.get_mission_by_id(m_id)[0])
    except Exception:
        raise ValueError
    if mission.status != "IN_PROGRESS":
        raise ValueError
    update_mission_status(m_id, MissionStatus.FAILED)
    assert mission.assigned_agent_id
    agent_manager.increment_failed(mission.assigned_agent_id)

def deactivate_agent(a_id:int):
    try:
        agent = Agent.model_validate(agent_manager.get_agent_by_id(a_id)[0])
    except ValidationError:
        raise
    if not agent.is_active:
        raise ValueError
    agent_manager.deactivate_agent(a_id)

