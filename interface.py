from enum import Enum
from models import Task

#enum of type of messages
class MessageType(Enum):
        INFO = "[INFO]"
        ERROR = "[ERROR]"
        SUCCESS = "[OK]"
        
class Interface:

    #Messages to print
    def message(self, message:str, level: MessageType = MessageType.INFO):
        print(f"{level.value}: {message}")
        
    def success(self, message:str):
        self.message(message, MessageType.SUCCESS)
    
    def error(self, message:str):
        self.message(message, MessageType.ERROR)

    def info(self, message:str):
        self.message(message, MessageType.INFO)
    
        
    #Task prints
    def print_tasks(self, tasks: list[Task]) -> None:
        
        #validation
        if not tasks:
            print("Not tasks found")
            return
        
        #template for header
        header = f"\n {'ID':<5} {'Title':<30} {'Description':<50} {'Status':<15}"
        print(header)
        print("-" * len(header))
        
        for t in tasks:
            print(self._format_task(t))
    
    def _format_task(self, task: Task) -> str:
        return (
            f"{task.id_task:<5}"
            f"{task.title:<30}"
            f"{task.description:<50}"
            f"{task.state.value.upper():<15}"
        )
        
        
    #confirmations
    def confirm_delete(self) -> bool:
        response = input("Are you sure you want to delete the task? (y/n): ").strip().lower()
        return response in ("y", "yes")