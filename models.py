from enum import Enum
from datetime import datetime, timezone
from dataclasses import dataclass, field
import sqlite3

#status of the task
class State(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    
    @classmethod
    def parse_state (cls, status:str) -> State:
        
        #validations
        if not isinstance(status, str):
            raise ValueError(f"{status} is not a string")
        
        status = status.lower().strip()
        
        #create a list of valid states
        valid_states = [s.value for s in cls]
        
        if status not in valid_states:
            raise ValueError((f"{status} is not a valid State. "
                             f"Valid states are: {valid_states}"))
        
        #if not errors, return
        return State(status)
        
    
#Class Task
@dataclass
class Task:
    #constants
    
    #atributes
    id_task: int
    title: str
    description: str
    state: State = State.TODO
    created: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated : str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    #parse from task to dict
    def to_dict(self) -> dict:
        return  {
            "id": self.id_task,
            "title": self.title,
            "description": self.description,
            "state": self.state.name,
            "created": self.created,
            "updated": self.updated
        }
        
    #create a task from a dict
    @classmethod
    def from_row(cls, row:sqlite3.Row):
        
        #create task
        task = cls(
            id_task = row["id"],
            title = row["title"],
            description = row["description"]
        )#end_constructor_Task
        task.state = State.parse_state(row["state"])
        task.created = row["created"]
        task.updated = row["updated"]
        
        return task
    
    #style to print the object
    def __str__(self) -> str:
        return (
            f"{self.id_task:<5}"
            f"{self.title:<30}"
            f"{self.description:<30}" 
            f"{self.state.value.upper():<10}"
        )
        
