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
            cur = conn.cursor()
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
            cur.execute("CREATE DATABASE IF NOT EXISTS `intelligence_db`;")

    

    def create_tables(self):
        with self.get_cursor() as cur:
            query_agents_table = """
                CREATE TABLE IF NOT EXISTS intelligence_db.agents(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50),
                    specialty VARCHAR(50),
                    is_active BOOLEAN DEFAULT TRUE,
                    completed_missions INT DEFAULT 0,
                    failed_missions INT DEFAULT 0,
                    agent_rank ENUM('Junior','Senior','Commander')
                );
                """
            query_missions_table = """
                CREATE TABLE IF NOT EXISTS intelligence_db.missions(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(50),
                    description TEXT,
                    location VARCHAR(50),
                    difficulty INT,
                    importance INT,
                    status VARCHAR(50),
                    risk_level VARCHAR(50),
                    assigned_agent_id INT NULL
                );
                """
            cur.execute(query_agents_table)
            cur.execute(query_missions_table)