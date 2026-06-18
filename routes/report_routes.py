from fastapi import APIRouter

import intelligence_unit
from create_logger import create_logger


report_router = APIRouter()
logger = create_logger(__name__)

@report_router.get("/summary/report")
def get_summary_report():
    logger.info("GET, /summary/report")
    data = {
        "active_agents_count": intelligence_unit.agent_manager.count_active_agents(),
        "total_missions": intelligence_unit.mission_manager.count_all_missions(),
        "open_missions": intelligence_unit.mission_manager.count_open_missions(),
        "completed_missions": intelligence_unit.mission_manager.count_by_status("COMPLETED"),
        "failed_missions": intelligence_unit.mission_manager.count_by_status("FAILED"),
        "critical_missions": intelligence_unit.mission_manager.count_critical_missions()
        }
    logger.info("summary built")
    return data


@report_router.get("/reports/missions-by-status")
def get_report_by_status():
    logger.info("GET, /reports/missions-by-status")
    data = {
        "open": intelligence_unit.mission_manager.count_open_missions(),
        "in_progress": intelligence_unit.mission_manager.count_by_status("IN_PROGRESS"),
        "completed": intelligence_unit.mission_manager.count_by_status("COMPLETED"),
        "failed": intelligence_unit.mission_manager.count_by_status("FAILED"),
        "cancelled": intelligence_unit.mission_manager.count_by_status("CANCELLED")
        }
    logger.info("dict by status built")
    return data

@report_router.get("/reports/top-agent")
def get_top_agent():
    logger.info("GET, /reports/top-agent")
    data = intelligence_unit.mission_manager.get_top_agent()
    logger.info("top agent retrieved")
    return data