#!/usr/bin/env python3
"""Simple todo application."""

import json
import os
from pathlib import Path

class TodoApp:
    def __init__(self, filename="todos.json"):
        self.filename = filename
        self.todos = self.load_todos()

    def load_todos(self):
        """Load todos from file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []

    def save_todos(self):
        """Save todos to file."""
        with open(self.filename, 'w') as f:
            json.dump(self.todos, f, indent=2)

    def add_todo(self, title, description=""):
        """Add a new todo."""
        todo = {
            "id": len(self.todos) + 1,
            "title": title,
            "description": description,
            "completed": False
        }
        self.todos.append(todo)
        self.save_todos()
        return todo

    def list_todos(self):
        """List all todos."""
        return self.todos

    def complete_todo(self, todo_id):
        """Mark a todo as completed."""
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["completed"] = True
                self.save_todos()
                return todo
        return None

    def delete_todo(self, todo_id):
        """Delete a todo by id."""
        self.todos = [t for t in self.todos if t["id"] != todo_id]
        self.save_todos()
        return True

    def get_stats(self):
        """Get todo statistics."""
        total = len(self.todos)
        completed = sum(1 for t in self.todos if t["completed"])
        pending = total - completed
        return {
            "total": total,
            "completed": completed,
            "pending": pending
        }

def main():
    app = TodoApp()

    # Example usage
    app.add_todo("Buy groceries", "Milk, eggs, bread")
    app.add_todo("Write documentation")
    app.add_todo("Review pull requests", "Check GitHub PRs")

    print("Todos:")
    for todo in app.list_todos():
        status = "✓" if todo["completed"] else "○"
        print(f"  {status} [{todo['id']}] {todo['title']}")

    print("\nStats:", app.get_stats())

    # Mark first todo as completed
    app.complete_todo(1)

    print("\nAfter completing first todo:")
    print("Stats:", app.get_stats())

if __name__ == "__main__":
    main()
