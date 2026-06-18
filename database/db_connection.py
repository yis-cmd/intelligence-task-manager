from contextlib import contextmanager

import mysql.connector

from database.db_config import Config


class DB_connection:
    config = Config()

    def get_connection(self):
        conn = mysql.connector.connect(**self.config.model_dump())
        return conn

    @contextmanager
    def get_cursor(self):
        conn = mysql.connector.connect(**self.config.model_dump())
        try:
            cur = conn.cursor(dictionary=True)
            yield cur
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
    
    
    def create_database(self):
        with self.get_cursor() as cur:
            cur.execute("CREATE DATABASE IF NOT EXISTS `Intelligence_db`;")

    

    def create_tables(self):
        with self.get_cursor() as cur:
            query_agents_table = """
                CREATE TABLE IF NOT EXISTS Intelligence_db.agents(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    specialty VARCHAR(50) NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    completed_missions INT DEFAULT 0,
                    failed_missions INT DEFAULT 0,
                    agent_rank ENUM('Junior','Senior','Commander')
                );
                """
            query_missions_table = """
                CREATE TABLE IF NOT EXISTS Intelligence_db.missions(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(50) NOT NULL,
                    description TEXT NOT NULL,
                    location VARCHAR(50) NOT NULL,
                    difficulty INT CHECK (difficulty BETWEEN 1 AND 10),
                    importance INT CHECK (importance BETWEEN 1 AND 10),
                    status VARCHAR(50) NOT NULL,
                    risk_level VARCHAR(50) NOT NULL,
                    assigned_agent_id INT NULL
                );
                """
            cur.execute(query_agents_table)
            cur.execute(query_missions_table)