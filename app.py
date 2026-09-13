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

class ProposalApp:
    def __init__(self, filename="proposals.json"):
        self.filename = filename
        self.proposals = self.load_proposals()

    def load_proposals(self):
        """Load proposals from file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []

    def save_proposals(self):
        """Save proposals to file."""
        with open(self.filename, 'w') as f:
            json.dump(self.proposals, f, indent=2)

    def add_proposal(self, title, description=""):
        """Add a new proposal, starting in the 'pending' status."""
        proposal = {
            "id": len(self.proposals) + 1,
            "title": title,
            "description": description,
            "status": "pending"
        }
        self.proposals.append(proposal)
        self.save_proposals()
        return proposal

    def list_proposals(self):
        """List all proposals."""
        return self.proposals

    def approve_proposal(self, proposal_id):
        """Mark a proposal as approved."""
        for proposal in self.proposals:
            if proposal["id"] == proposal_id:
                proposal["status"] = "approved"
                self.save_proposals()
                return proposal
        return None

    def reject_proposal(self, proposal_id):
        """Mark a proposal as rejected."""
        for proposal in self.proposals:
            if proposal["id"] == proposal_id:
                proposal["status"] = "rejected"
                self.save_proposals()
                return proposal
        return None

    def delete_proposal(self, proposal_id):
        """Delete a proposal by id."""
        self.proposals = [p for p in self.proposals if p["id"] != proposal_id]
        self.save_proposals()
        return True

    def get_stats(self):
        """Get proposal statistics."""
        total = len(self.proposals)
        approved = sum(1 for p in self.proposals if p["status"] == "approved")
        rejected = sum(1 for p in self.proposals if p["status"] == "rejected")
        pending = total - approved - rejected
        return {
            "total": total,
            "approved": approved,
            "rejected": rejected,
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

    proposals = ProposalApp()

    proposals.add_proposal("Redesign homepage", "Refresh layout and branding")
    proposals.add_proposal("Add dark mode")

    print("\nProposals:")
    for proposal in proposals.list_proposals():
        print(f"  [{proposal['id']}] {proposal['title']} ({proposal['status']})")

    proposals.approve_proposal(1)

    print("\nAfter approving first proposal:")
    print("Stats:", proposals.get_stats())

if __name__ == "__main__":
    main()
