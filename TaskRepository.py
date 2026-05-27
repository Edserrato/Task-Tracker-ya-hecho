from database import Database
from models import State
import sqlite3

class TaskRepository:
    
    #init
    def __init__(self, db:Database) -> None:
        self.db = db
    
    #insert row to db
    def add(self, title:str, description:str):
        self.db.cursor.execute("INSERT INTO tasks (title, description, state) VALUES (?, ?, ?)",
                               (title, description, State.TODO.value))
        
        self.db.conn.commit()
        
    #update row in db
    def update(self, task_id: int,  params:dict):
        
        #set query
        set_clause = ", ".join(f"{p} = ?" for p in params)
        query = f"UPDATE tasks SET updated = CURRENT_TIMESTAMP, {set_clause}  WHERE id = ?"
        
        #copy values and add task id
        values = list(params.values())
        values.append(task_id)
        
        #execute sql and saves
        self.db.cursor.execute(query, tuple(values))
        self.db.conn.commit()
        
    #get a single row
    def get(self, task_id:int ) -> sqlite3.Row:
        self.db.cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))    
        return self.db.cursor.fetchone()
        
    #get all row
    def get_all(self, params:dict, num:int = 0) -> list:
        query = "SELECT * FROM tasks "
        
        
        #validations
        if params:
            query += "WHERE " + " AND ".join(f"{p} = ?" for p in params)
        
        values = list(params.values())
        
        if num:
            query += " LIMIT ?"
            values.append(num)
        
        #sql
        self.db.cursor.execute(query, tuple(values))
        return self.db.cursor.fetchall()
    
    #delete row
    def delete(self, task_id: int):
        self.db.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.db.conn.commit()
        