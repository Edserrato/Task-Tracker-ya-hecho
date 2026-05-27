import sqlite3 as sql

class Database:
    def __init__(self) -> None:
        self.conn = sql.connect("db_tasks.db")
        self.conn.row_factory = sql.Row
        self.cursor = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
        #execute
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            state TEXT NOT NULL DEFAULT 'todo',
            created TEXT DEFAULT CURRENT_TIMESTAMP,
            updated TEXT DEFAULT CURRENT_TIMESTAMP
        )
                            """) #end execute
        
        self.conn.commit()
        

