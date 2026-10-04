#!/usr/bin/env python3
"""Tests for the todo application."""

import os
import json
import tempfile
from app import TodoApp, ProposalApp

def test_delete_todo():
    """Test deleting a todo."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test_todos.json")
        app = TodoApp(test_file)

        # Add some todos
        app.add_todo("Task 1")
        app.add_todo("Task 2")
        app.add_todo("Task 3")

        assert len(app.list_todos()) == 3

        # Delete a todo
        app.delete_todo(2)

        todos = app.list_todos()
        assert len(todos) == 2
        assert all(t["id"] != 2 for t in todos)
        assert any(t["id"] == 1 for t in todos)
        assert any(t["id"] == 3 for t in todos)

        print("✓ delete_todo test passed")

def test_delete_nonexistent():
    """Test deleting a non-existent todo."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test_todos.json")
        app = TodoApp(test_file)

        app.add_todo("Task 1")
        initial_count = len(app.list_todos())

        # Try to delete non-existent todo
        app.delete_todo(999)

        # Should still have same count
        assert len(app.list_todos()) == initial_count
        print("✓ delete_nonexistent test passed")

def test_proposal_lifecycle():
    """Test adding, approving, and rejecting proposals."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test_proposals.json")
        app = ProposalApp(test_file)

        app.add_proposal("Proposal 1")
        app.add_proposal("Proposal 2")
        app.add_proposal("Proposal 3")

        assert len(app.list_proposals()) == 3
        assert all(p["status"] == "pending" for p in app.list_proposals())

        app.approve_proposal(1)
        app.reject_proposal(2)

        proposals = {p["id"]: p for p in app.list_proposals()}
        assert proposals[1]["status"] == "approved"
        assert proposals[2]["status"] == "rejected"
        assert proposals[3]["status"] == "pending"

        stats = app.get_stats()
        assert stats == {"total": 3, "approved": 1, "rejected": 1, "pending": 1}

        print("✓ proposal_lifecycle test passed")

def test_delete_proposal():
    """Test deleting a proposal."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test_proposals.json")
        app = ProposalApp(test_file)

        app.add_proposal("Proposal 1")
        app.add_proposal("Proposal 2")

        app.delete_proposal(1)

        proposals = app.list_proposals()
        assert len(proposals) == 1
        assert proposals[0]["id"] == 2

        print("✓ delete_proposal test passed")

if __name__ == "__main__":
    test_delete_todo()
    test_delete_nonexistent()
    test_proposal_lifecycle()
    test_delete_proposal()
    print("\nAll tests passed!")
