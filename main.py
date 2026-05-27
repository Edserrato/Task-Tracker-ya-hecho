from TaskManager import TaskManager
import cli
from interface import Interface
from TaskRepository import TaskRepository
from database import Database

def main():
    
    db = Database()
    
    repository = TaskRepository(db)
    manager = TaskManager(repository)
    
    inter = Interface()
    
    cli.run_cli(manager, inter)
    
if __name__ == "__main__":
    main()