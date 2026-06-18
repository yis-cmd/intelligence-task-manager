from fastapi import APIRouter, HTTPException

from database.agent_db import AgentNotExistsError
from database.base_models import MissionCreate
from database.mission_db import MissionNotExistsError
import intelligence_unit
from create_logger import create_logger

missions_router = APIRouter()
logger = create_logger(__name__)

@missions_router.post("/missions", status_code=201)
def create_mission(data:MissionCreate):
    return intelligence_unit.mission_manager.create_mission(data)

@missions_router.get("/missions")
def get_all_mission():
    return intelligence_unit.mission_manager.get_all_missions()

@missions_router.get("/missions/{id}")
def get_mission_by_id(id:int):
    try:
        return intelligence_unit.mission_manager.get_mission_by_id(id)
    except MissionNotExistsError:
        raise HTTPException(404, "mission not found")

@missions_router.put("/missions/{id}/assign/{agent_id}")
def assign_mission(id:int, agent_id:int):
    try:
        intelligence_unit.assign_mission(id, agent_id)
        return {"success": "mission assigned"}
    except MissionNotExistsError:
        raise HTTPException(404, "Mission not found")
    except AgentNotExistsError:
        raise HTTPException(404, "Agent not found")
    except intelligence_unit.TooManyMissionsError:
        raise HTTPException(400, "Agent has reached maximum missions")
    except intelligence_unit.MissionAlreadyAssignedError:
        raise HTTPException(400, "Mission not available")
    except intelligence_unit.AgentInactiveError:
        raise HTTPException(400, "Agent is not active")
    except intelligence_unit.AgentNotAuthorizedError:
        raise HTTPException(400, "Only Commander can handle critical missions")

@missions_router.put("/missions/{id}/start")
def start_mission(id:int):
    try:
        intelligence_unit.start_mission(id)
        return "success"
    except MissionNotExistsError:
        raise HTTPException(404, "Mission not found")
    except intelligence_unit.InvalidUpdateStatusError:
        raise HTTPException(400, "can only start assigned missions")
    
@missions_router.put("/missions/{id}/complete")
def success_complete_mission(id:int):
    try:
        intelligence_unit.complete_mission(id)
        return "success"
    except MissionNotExistsError:
        raise HTTPException(404, "Mission not found")
    except intelligence_unit.InvalidUpdateStatusError:
        raise HTTPException(400, "can only complete in_progress missions")
    
@missions_router.put("/missions/{id}/fail")
def failed_mission(id:int):
    try:
        intelligence_unit.failed_mission(id)
        return "success"
    except MissionNotExistsError:
        raise HTTPException(404, "Mission not found")
    except intelligence_unit.InvalidUpdateStatusError:
        raise HTTPException(400, "can only fail in_progress missions")

@missions_router.put("/missions/{id}/cancel")
def cancel_mission(id:int):
    try:
        intelligence_unit.cancel_mission(id)
        return "success"
    except MissionNotExistsError:
        raise HTTPException(404, "Mission not found")
    except intelligence_unit.InvalidUpdateStatusError:
        raise HTTPException(400, "cannot cancel mission after it started")