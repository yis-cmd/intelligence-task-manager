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
    logger.info("POST, /missions")
    mission = intelligence_unit.mission_manager.create_mission(data)
    logger.info(f"created mission: id={mission.id}")
    return mission

@missions_router.get("/missions")
def get_all_mission():
    logger.info("GET, /missions")
    missions =  intelligence_unit.mission_manager.get_all_missions()
    logger.info("missions list built")
    return missions

@missions_router.get("/missions/{id}")
def get_mission_by_id(id:int):
    logger.info(f"GET, /missions{id}")
    try:
        mission = intelligence_unit.mission_manager.get_mission_by_id(id)
        logger.info(f"found mission: id={id}")
        return mission
    except MissionNotExistsError:
        logger.error(f"Mission not found: {id}")
        raise HTTPException(404, "mission not found")

@missions_router.put("/missions/{id}/assign/{agent_id}")
def assign_mission(id:int, agent_id:int):
    logger.info(f"PUT, /missions/{id}/assign/{agent_id}")
    try:
        intelligence_unit.assign_mission(id, agent_id)
        logger.info(f"mission {id} assigned to {agent_id}")
        return {"success": "mission assigned"}
    except MissionNotExistsError:
        logger.error(f"Mission not found: {id}")
        raise HTTPException(404, "Mission not found")
    except AgentNotExistsError:
        logger.error(f"Agent not found: {agent_id}")
        raise HTTPException(404, "Agent not found")
    except intelligence_unit.TooManyMissionsError:
        logger.error(f"Agent has reached maximum missions: id={agent_id}")
        raise HTTPException(400, "Agent has reached maximum missions")
    except intelligence_unit.MissionAlreadyAssignedError:
        logger.error(f"mission {id} already assigned")
        raise HTTPException(400, "Mission not available")
    except intelligence_unit.AgentInactiveError:
        logger.error(f"cannot assign to inactive agent {agent_id}")
        raise HTTPException(400, "Agent is not active")
    except intelligence_unit.AgentNotAuthorizedError:
        logger.error(f"agent {agent_id} cannot be assigned critical missions")
        raise HTTPException(400, "Only Commander can handle critical missions")

@missions_router.put("/missions/{id}/start")
def start_mission(id:int):
    logger.info(f"PUT, /missions/{id}/start")
    try:
        intelligence_unit.start_mission(id)
        logger.info(f"mission {id} started")
        return "started"
    except MissionNotExistsError:
        logger.error(f"Mission not found: {id}")
        raise HTTPException(404, "Mission not found")
    except intelligence_unit.InvalidUpdateStatusError:
        logger.error(f"mission {id} was not status assigned")
        raise HTTPException(400, "can only start assigned missions")
    
@missions_router.put("/missions/{id}/complete")
def success_complete_mission(id:int):
    logger.info(f"PUT, /missions/{id}/complete")
    try:
        intelligence_unit.complete_mission(id)
        logger.info(f"mission {id} completed")
        return "completed"
    except MissionNotExistsError:
        logger.error(f"Mission not found: {id}")
        raise HTTPException(404, "Mission not found")
    except intelligence_unit.InvalidUpdateStatusError:
        logger.error(f"mission {id} was not in_progress")
        raise HTTPException(400, "can only complete in_progress missions")
    
@missions_router.put("/missions/{id}/fail")
def failed_mission(id:int):
    logger.info(f"PUT, /missions/{id}/fail")
    try:
        intelligence_unit.failed_mission(id)
        logger.info(f"mission {id} failed")
        return "failed"
    except MissionNotExistsError:
        logger.error(f"Mission not found: {id}")
        raise HTTPException(404, "Mission not found")
    except intelligence_unit.InvalidUpdateStatusError:
        logger.error("mission was not in_progress")
        raise HTTPException(400, "can only fail in_progress missions")

@missions_router.put("/missions/{id}/cancel")
def cancel_mission(id:int):
    logger.info(f"PUT, /missions/{id}/cancel")
    try:
        intelligence_unit.cancel_mission(id)
        logger.info(f"mission {id} cancelled")
        return "cancelled"
    except MissionNotExistsError:
        logger.error(f"Mission not found: {id}")
        raise HTTPException(404, "Mission not found")
    except intelligence_unit.InvalidUpdateStatusError:
        logger.error(f"mission {id} cannot be cancelled")
        raise HTTPException(400, "cannot cancel mission after it started")