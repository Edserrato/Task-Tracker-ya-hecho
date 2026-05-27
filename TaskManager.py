import copy
from models import Task
from models import State
from TaskRepository import TaskRepository

class TaskManager:
    #constants
    FILE_NAME = "CLITasks.json"
    
    
    #get a single task
    def _get(self, id_task: int) -> Task:
    
        #get task from db and validates
        row = self.repository.get(id_task)
        
        #validation
        if not row:
            raise KeyError(f"Task with id: {id_task} not found!")
        
        #creates a Task and returns
        return Task.from_row(row)
    
    #validate int
    def _valid_int(self, task_id:int):
        if task_id <= 0:
            raise ValueError("Id cannot be negative or zero")
    
    #validate strings
    def _validate_string(self, text:str):
        
        if not isinstance(text, str):
            raise TypeError(f"{text} is not valid.")
        
        text = text.strip()
        
        if not text:
            raise ValueError("Text cannot be empty or just spaces")
        return text
      
    #innit
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository
    
    #add task        
    def add(self, title:str, description:str):
        #validations
        title_valid = self._validate_string(title)
        description_valid = self._validate_string(description)
        
        #insert task
        self.repository.add(title_valid, description_valid)
    #show tasks 
    def get_all(self, status_task:str, num_tasks_to_show:int = 0) -> list:
        params = {}
        
        #validations
        if status_task:
            valid_status_task = self._validate_string(status_task)
            state = State.parse_state(valid_status_task)
            params["state"] = state.value
        
        #sql
        row_tasks = self.repository.get_all(params, num_tasks_to_show)
        
        #Validate if exists rows
        if not row_tasks:
            raise KeyError("Not tasks found.")
        
        #convert to task
        tasks = [Task.from_row(r) for r in row_tasks]
        
        #return
        return tasks
        
    #delete task
    def delete(self, del_id: int) -> Task:
        
        #validations
        self._valid_int(del_id)
        task = self._get(del_id)
        
        #sql
        self.repository.delete(del_id)
        
        #return deleted task
        return task
            
    #update task. If not argument given, the properties of the task remains the same
    def update(self, task_id: int = 0, title: str = "", description: str = "", state:str = "") -> tuple[Task, Task] :
        
        #validate the task exists and saves it
        self._valid_int(task_id)
        og_task = copy.deepcopy(self._get(task_id))
            
        #validate fields and added list to update row
        values = {}
        
        if title:
            title_valid = self._validate_string(title)
            values["title"] = title_valid
             
        if description:
            description_valid = self._validate_string(description)
            values["description"] = description_valid
        
        if state:
            valid_state = State.parse_state(state)
            values["state"] = valid_state.value
        
        if not values:
            raise ValueError("Nothing to update")
        
        #execute sql
        self.repository.update(task_id, values)
        
        #get the new task
        new_task = self._get(task_id)
        
        #return the task
        return og_task, new_task
        
    