from database import db_connection

a = db_connection.DB_connection()
a.create_database()
a.create_tables()