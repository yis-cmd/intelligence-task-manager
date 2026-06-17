

from database.base_models import (
    Agent,
    AgentRank,
    Mission,
    AgentCreate,
    MissionCreate,
    MissionStatus,
)
from database.mission_db import MissionDB
from database.agent_db import AgentDB
import intelligence_unit

agent_manager = AgentDB()
mission_manager = MissionDB()

# mission_manager.create_mission(
#     MissionCreate(
#         title="gvs",
#         description="rre",
#         location="d",
#         difficulty=3,
#         importance=9,
#         status=MissionStatus.NEW,
#     )
# )

