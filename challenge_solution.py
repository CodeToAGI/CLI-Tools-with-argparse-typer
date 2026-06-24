"""
CodeToAGI — Episode 49 Challenge Solution
Todo List CLI with argparse + typer versions
"""

import argparse
import json
from pathlib import Path
from typing import List

TODO_FILE = Path("todos.json")

def load_todos() -> List[dict]:
    if TODO_FILE.exists():
        return json.loads(TODO_FILE.read_text())
    return []

def save_todos(todos: List[dict]):
    TODO_FILE.write_text(json.dumps(todos, indent=2))

# ==================== ARGparse VERSION ====================

def main_argparse():
    parser = argparse.ArgumentParser(description="Simple Todo List CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("task", type=str, help="Task description")

    # List command
    subparsers.add_parser("list", help="List all tasks")

    # Done command
    done_p = subparsers.add_parser("done", help="Mark task as done")
    done_p.add_argument("index", type=int, help="Task index (starting from 1)")

    args = parser.parse_args()

    todos = load_todos()

    if args.command == "add":
        todos.append({"task": args.task, "done": False})
        save_todos(todos)
        print(f"✅ Added: {args.task}")

    elif args.command == "list":
        if not todos:
            print("No tasks yet.")
            return
        for i, todo in enumerate(todos, 1):
            status = "✅" if todo["done"] else "⏳"
            print(f"{i}. {status} {todo['task']}")

    elif args.command == "done":
        if 1 <= args.index <= len(todos):
            todos[args.index-1]["done"] = True
            save_todos(todos)
            print(f"✅ Marked task {args.index} as done")
        else:
            print("Invalid task number")

# ==================== TYPER VERSION (Modern) ====================

import typer

app = typer.Typer(help="Simple Todo List CLI")

@app.command()
def add(task: str):
    """Add a new task"""
    todos = load_todos()
    todos.append({"task": task, "done": False})
    save_todos(todos)
    typer.echo(f"✅ Added: {task}")

@app.command()
def list():
    """List all tasks"""
    todos = load_todos()
    if not todos:
        typer.echo("No tasks yet.")
        return
    for i, todo in enumerate(todos, 1):
        status = "✅" if todo["done"] else "⏳"
        typer.echo(f"{i}. {status} {todo['task']}")

@app.command()
def done(index: int):
    """Mark a task as done"""
    todos = load_todos()
    if 1 <= index <= len(todos):
        todos[index-1]["done"] = True
        save_todos(todos)
        typer.echo(f"✅ Marked task {index} as done")
    else:
        typer.echo("Invalid task number")

if __name__ == "__main__":
    # Run argparse version
    # main_argparse()

    # Run typer version (recommended)
    app()
