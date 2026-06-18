from fastapi import APIRouter

import intelligence_unit


report_router = APIRouter()

@report_router.get("/summary/report")
def get_summary_report():
    return {
        "active_agents_count": intelligence_unit.agent_manager.count_active_agents(),
        "total_missions": intelligence_unit.mission_manager.count_all_missions(),
        "open_missions": intelligence_unit.mission_manager.count_open_missions(),
        "completed_missions": intelligence_unit.mission_manager.count_by_status("COMPLETED"),
        "failed_missions": intelligence_unit.mission_manager.count_by_status("FAILED"),
        "critical_missions": intelligence_unit.mission_manager.count_by_status("CANCELLED")
        }


@report_router.get("/reports/missions-by-status")
def get_report_by_status():
    return {
        "open": intelligence_unit.mission_manager.count_open_missions(),
        "in_progress": intelligence_unit.mission_manager.count_by_status("IN_PROGRESS"),
        "completed": intelligence_unit.mission_manager.count_by_status("COMPLETED"),
        "failed": intelligence_unit.mission_manager.count_by_status("FAILED"),
        "cancelled": intelligence_unit.mission_manager.count_by_status("CANCELLED")
        }

@report_router.get("/reports/top-agent")
def get_top_agent():
    return intelligence_unit.mission_manager.get_top_agent()