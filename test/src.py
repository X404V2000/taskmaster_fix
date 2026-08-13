import json
import os

# File to store tasks
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from the JSON file."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def add_task(descripion):
    """Add a new task."""
    tasks = load_tasks()
    new_id = len(tasks) + 1
    task = {"id": new_id, "description": descripion, "completed": False}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{descripion}' added with ID {new_id}.")

def list_tasks():
    """Display all tasks."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        status = "✓" if task.completed else "✗"
        print(f"[{status}] {task['id']}: {task['description']}")

def complete_task(task_id):
    """Mark a task as completed."""
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task.completed = True
            save_tasks(tasks)
            print(f"Task {task_id} marked as completed.")
            return
    print(f"Task {task_id} not found.")

def delete_task(task_id):
    """Delete a task."""
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Task {task_id} deleted.")
            return
    print(f"Task {task_id} not found.")

def main():
    while True:
        print("\n--- TaskMaster CLI ---")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            desc = input("Enter task description: ")
            add_task(desc)
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            try:
                task_id = int(input("Enter task ID to complete: "))
            except ValueError:
                print("Invalid ID. Please enter a number.")
            complete_task(task_id)
        elif choice == "4":
            task_id = int(input("Enter task ID to delete: "))
            delete_task(task_id)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
