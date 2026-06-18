# intelligence-task-manager

this system manages soldiers and missions of an intelligence unit

## database tables

### agents

id, int auto_increment pk, identity
name, varchar, the agent's name
specialty, varchar, agent's specialty field
is_active, boolean, default true
completed_missions, int, default 0
failed_missions, int, default 0
agent_rank, enum, can be only one of Junior/Senior/Commander

### missions

#### structure

id, int auto_increment pk, identity
title, varchar, mission's title
description, text, detailed description
location, varchar, location
difficulty, int, can only be 10-1
importance, int, can only be 10-1
status, varchar, default new
risk_level, varcahr, auto generated
assigned_agent_id, int, null at the start

##### the equation to generate risk_level is

difficulty \* 2 + importance
1-9 > low, 10-17 > medium, 18-24 > high, 25+ > critical

##### possible status

new, new mission default
assigned, been assigned an agent
in_progress, in progress
completed, completed successfully
failed, failed
cancelled, cancelled

## models

### DB_connection

manages connections

get_connection(), returns an active connection to mysql
get_cursor(), returns an active cursor to mysql
create_database(), creates Intelligence_db if not exists
create_tables(), creates both tables if not exists

both create_database and create_tables run when the program loads

### AgentDB

manages agents

create_agent(data), creates a new agent returns its object
get_all_agents(), returns a list of all agents
get_agent_by_id(id), returns an agent by id
update_agent(id, data), updates the agent (cannot update the id) returns state
deactivate_agent(id), sets is_active false returns state
increment_completed(id), updates completed_missions returns state
increment_failed(id), updates completed_missions returns state
get_agent_performance(id), returns dict with the keys (completed, failed, total, success rate)
count_active_agents(), returns active agents count

### MissionDB

manages missions

create_mission(data), creates a new mission returns the mission object
get_all_missions(), returns the full missions list
get_mission_by_id(id), returns a mission data by id
assign_mission(m_id, a_id), assign an agent to a mission returns state
update_mission_status(id, status), changes a mission's status returns state
get_open_missions_by_agent(id), returns missions assigned to the agent
count_all_missions(), returns count of all the missions
count_by_status(), returns a count of all missions with the status
count_open_missions(), returns open missions count
count_critical_missions(), returns critical missions count

### BaseRepository

generic sql requests class

\_execute(query, values), execute a query returns the fetchall result
select(table_name, filters), returns the selected objects list
insert(table_name, data), inserts the data returns the data
update(table_name, data, filters) updates the data returns the modified data
count(table_name, filters), returns row count by filters

### base_models.py

defines the system's objects's structure

### intelligence unit

service module connects between the server layer to the db layer

### config.env

environment configurations

### config.py

environment configurations file handler

## endpoints

### agents router

1. POST, /agents, create new agent
2. GET, /agents, get all agents
3. GET, /agents/{id}, get agent by id
4. PUT, /agents/{id}, update agent by id
5. PUT, /agents/{id}/deactivate, deactivate agent
6. GET, /agents/{id}/performance, get agent performance

### missions router

1. POST, /missions, create mission
2. GET, /missions, get all missions
3. GET, /missions/{id}, get mission by id
4. PUT, /missions/{id}/assign/{agent_id}, assign mission to agent
5. PUT, /missions/{id}/start, start mission
6. PUT, /missions/{id}/complete, complete mission successfully
7. PUT, /missions/{id}/fail, finish mission failed
8. PUT, /missions/{id}/cancel, cancel mission

### reports router

1. GET, /summary/report, general summary
2. GET, /reports/missions-by-status, missions by status
3. GET, /reports/top-agent, get top agent

#### examples reports

##### general summary

{
"active_agents_count": 0,
"total_missions": 0,
"open_missions": 0,
"completed_missions": 0,
"failed_missions": 0,
"critical_missions": 0
}

##### mission by status

{
"open": 5,
"in_progress": 3,
"completed": 12,
"failed": 1,
"critical": 2
}

## business rules

1. rank has to be Commander / Senior / Junior returns error otherwise
2. difficulty and importance have to be between 1-10 raise error otherwise
3. risk_level is auto generated the user cannot send it
4. agent with is_active=False cannot be assigned missions
5. an agent cannot be assigned more than 3 open missions at a time
6. only a commander can get a mission with risk_level = Critical
7. only a mission with status=new can be assigned, status becomes assigned
8. only a mission with status=assigned can be started, status becomes in_progress
9. only a mission with status=in_progress can be finished, status becomes failed/completed
10. only a mission with status=new/assigned can be cancelled error otherwise

## how to run the project (linux)

1. create docker container: docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
2. clone the repository: git clone https://github.com/yis-cmd/intelligence-task-manager
3. enter the project dir: cd intelligence-task-manager
4. create a python venv: python3.14 -m venv venv
5. activate the venv: source venv/bin/activate
6. install the dependencies: pip install -r requirements.txt
7. start the server: uvicorn main:app

"a change so i can do the last commit"
