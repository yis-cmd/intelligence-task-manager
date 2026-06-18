from fastapi import APIRouter, HTTPException


from database.agent_db import AgentNotExistsError
from database.base_models import AgentCreate, AgentUpdate
import intelligence_unit
from create_logger import create_logger

agents_router = APIRouter()
logger = create_logger(__name__)

@agents_router.post("/agents", status_code=201)
def create_agent(data:AgentCreate):
    logger.info("POST, /agents")
    agent = intelligence_unit.agent_manager.create_agent(data)
    logger.info(f"Agent created successfully: id={agent.id}")
    return agent
    
    

@agents_router.get("/agents")
def get_all_agents():
    logger.info("GET, /agents")
    agents = intelligence_unit.agent_manager.get_all_agents()
    logger.info("got list of agents")
    return agents

@agents_router.get("/agents/{id}")
def get_agent_by_id(id:int):
    logger.info(f"GET, /agents/{id}")
    try:
        agent = intelligence_unit.agent_manager.get_agent_by_id(id)
        logger.info(f"found agent id={id}")
        return agent
    except AgentNotExistsError:
        logger.error(f"Agent not found: {id}")
        raise HTTPException(404, "agent not found")
    
@agents_router.put("/agents/{id}")
def update_agent(id:int, data:AgentUpdate):
    try:
        logger.info(f"PUT, /agents/{id}")
        intelligence_unit.agent_manager.update_agent(id, data)
        logger.info(f"updated agent id={id}")
        return {"success": "agent updated"}
    except AgentNotExistsError:
        logger.error(f"Agent not found: {id}")
        raise HTTPException(404, "agent not found")
    
@agents_router.put("/agents/{id}/deactivate")
def deactivate_agent(id:int):
    logger.info(f"PUT, /agents/{id}/deactivate")
    try:
        intelligence_unit.deactivate_agent(id)
        logger.info(f"deactivated agent id={id}")
    except AgentNotExistsError:
        logger.error(f"Agent not found: {id}")
        raise HTTPException(404, "agent not found")
    except intelligence_unit.AgentInactiveError:
        logger.error(f"agent already inactive: {id}")
        raise HTTPException(400, "agent already inactive")
    
@agents_router.get("/agents/{id}/performance")
def get_agent_performance(id:int):
    logger.info(f"GET, /agents/{id}/performance")
    try:
        performance = intelligence_unit.agent_manager.get_agent_performance(id)
        logger.info(f"got agent performance: id={id}")
        return performance
    except AgentNotExistsError:
        logger.error(f"Agent not found: {id}")
        raise HTTPException(404, "agent not found")