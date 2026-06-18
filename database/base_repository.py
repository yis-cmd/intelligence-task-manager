from typing import Any

from database.base_models import Agent, AgentUpdate, MissionUpdate
from database.db_connection import DB_connection


def secure_identifier(identifier: str):
    return f"`{identifier.replace('`', '``')}`"


def secure_identifiers(identifiers: list[str]):
    return ", ".join(secure_identifier(i) for i in identifiers)


def format_filters(filters: dict[str, Any]):
    filters_str = " AND ".join(f"{f} = %s" for f in filters)
    values = list(filters.values())
    return filters_str, values


def format_updates(updates: dict[str, Any]):
    updates_str = ", ".join(f"{f} = %s" for f in updates)
    values = list(updates.values())
    return updates_str, values


class BaseRepository:
    def __init__(self) -> None:
        self.connection_pool = DB_connection()

    def _execute(self, query: str, values: list | None = None):
        if not values:
            values = []
        with self.connection_pool.get_cursor() as cur:
            cur.execute("USE Intelligence_db;")
            cur.execute(f"{query};", values)
            data = cur.fetchall()
        return data

    def select(self, table_name: str, filters: dict[str, Any] | None = None):
        query = f"SELECT * FROM {secure_identifier(table_name)}"
        values = []
        if filters:
            filters_str, values = format_filters(filters)
            query += " WHERE " + filters_str
        data = self._execute(query, values)
        return data

    def insert(self, table_name: str, data: dict[str, Any]):
        columns = list(data)
        values = list(data.values())
        query = f"INSERT INTO {secure_identifier(table_name)} ({secure_identifiers(columns)}) VALUES ({", ".join(["%s"]*len(values))})"
        self._execute(query, values)

    def update(self, table_name: str, update_data: MissionUpdate | AgentUpdate, filters: dict[str, Any] | None = None):
        data = update_data.model_dump(exclude_none=True)
        values = []
        updates_str, updates_values = format_updates(data)
        values += updates_values
        query = f"UPDATE {secure_identifier(table_name)} SET {updates_str}"
        if filters:
            filters_str, filters_values = format_filters(filters)
            query += " WHERE " + filters_str
            values += filters_values
        self._execute(query, values)

    def count(self, table_name: str, filters: dict[str, Any] | None = None):
        query = f"SELECT COUNT(*) FROM {secure_identifier(table_name)}"
        values = []
        if filters:
            filters_str, values = format_filters(filters)
            query += " WHERE " + filters_str
        response = self._execute(query, values)
        return response[0]['COUNT(*)'] #type: ignore
