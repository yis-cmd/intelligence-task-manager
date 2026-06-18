from fastapi import APIRouter, HTTPException


from database.agent_db import AgentNotExistsError
from database.base_models import AgentCreate, AgentUpdate
import intelligence_unit
from create_logger import create_logger

agents_router = APIRouter()
logger = create_logger(__name__)

@agents_router.post("/agents", status_code=201)
def create_agent(data:AgentCreate):
    return intelligence_unit.agent_manager.create_agent(data)
    

@agents_router.get("/agents")
def get_all_agents():
    return intelligence_unit.agent_manager.get_all_agents()

@agents_router.get("/agents/{id}")
def get_agent_by_id(id:int):
    try:
        return intelligence_unit.agent_manager.get_agent_by_id(id)
    except AgentNotExistsError:
        raise HTTPException(404, "agent not found")
    
@agents_router.put("/agents/{id}")
def update_agent(id:int, data:AgentUpdate):
    intelligence_unit.agent_manager.update_agent(id, data)
    return {"success": "agent updated"}
    
@agents_router.put("/agents/{id}/deactivate")
def deactivate_agent(id:int):
    try:
        intelligence_unit.deactivate_agent(id)
    except AgentNotExistsError:
        raise HTTPException(404, "agent not found")
    except intelligence_unit.AgentInactiveError:
        raise HTTPException(400, "agent already inactive")
    
@agents_router.get("/agents/{id}/performance")
def get_agent_performance(id:int):
    try:
        return intelligence_unit.agent_manager.get_agent_performance(id)
    except AgentNotExistsError:
        raise HTTPException(404, "agent not found")