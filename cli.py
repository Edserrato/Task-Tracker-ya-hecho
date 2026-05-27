from models import State
from interface import Interface
from TaskManager import TaskManager
import argparse
    
  
def run_cli(manager: TaskManager, interface: Interface):
    parser = argparse.ArgumentParser(description="CLI Task Tracker")
    sub_parser = parser.add_subparsers(dest="commands", help="available actions")
    
    #handler add
    def add_handler(manager: TaskManager, args):
        try:
            manager.add(args.title, args.description)
            interface.success(f"Task: '{args.title}' added!")
        except ValueError as e:
            interface.error(str(e))
        
    #add command
    add_parser = sub_parser.add_parser("add", help="add a new task")
    add_parser.add_argument("title", help="title of task", type=str)
    add_parser.add_argument("description", help="description of task", type=str)
    add_parser.set_defaults(func=add_handler)
    
    #handler del
    def del_handler(manager: TaskManager, args):
        try:
            if interface.confirm_delete():
                manager.delete(args.id_task)
                interface.success("Task deleted")
        except KeyError as e:
            interface.error(str(e))
            
            
    #delete command
    del_parser = sub_parser.add_parser("rm", help="delete a task")
    del_parser.add_argument("id_task", help="id task to delete", type=int)
    del_parser.set_defaults(func=del_handler)
    
    #handler edit
    def update_handler(manager: TaskManager, args):
        try:
            old_task, _ = manager.update(args.id_task, args.title, args.description, args.status)
            interface.success(f"Task: {old_task.title} updated.")
        except (KeyError) as e:
            interface.error(str(e))
    
    #update task
    edit_parser = sub_parser.add_parser("update", help="edit title and desc")
    edit_parser.add_argument("id_task", help="id task to edit", type=int)
    edit_parser.add_argument("-t", "--title", help="new title", type=str)
    edit_parser.add_argument("-d","--description", help="new descript for task", type=str)
    edit_parser.add_argument("-s","--status", help=f"new status of the task. Valid Options: {[s.value for s in State]} ", type=str)
    edit_parser.set_defaults(func=update_handler)
    
    
    #handler show tasks
    def show_tasks_handler(manager: TaskManager, args):
        try:
            tasks = manager.get_all(args.status, args.number)
            interface.print_tasks(tasks)
        except (KeyError) as e:
            interface.info(str(e))
        
    
    show_parser = sub_parser.add_parser("show", help="show all tasks")
    show_parser.add_argument("-s", "--status", type=str, help= f"filter by: {[s.value for s in State]}")
    show_parser.add_argument("-n", "--number", default = 0, type=int, help= "number of tasks to show" )
    show_parser.set_defaults(func=show_tasks_handler)
    
    
    #complete <id>
    def complete_task_handler(manager: TaskManager, args):
        try:
            old_task, _ = manager.update(args.id_task, state="done")
            interface.success(f"Task '{old_task.title}' completed.")
        except KeyError as e:
            interface.error(str(e))
        
    completed_parser = sub_parser.add_parser("complete", help="mark a task as done")
    completed_parser.add_argument("id_task", type=int, help="id of task" )
    completed_parser.set_defaults(func=complete_task_handler)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(manager, args)
    else:
        parser.print_help()

