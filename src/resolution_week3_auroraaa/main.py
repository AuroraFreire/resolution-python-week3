from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
from datetime import date
import uvicorn


app = FastAPI()


TASKS_FILE = "tasks.json"


class TaskBody(BaseModel):
    task: str
    notes: str = ""
    due_date: str = None


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)


@app.get("/tasks")
async def get_tasks():
    return load_tasks()


@app.post("/tasks")
async def add_task(body: TaskBody):
    tasks = load_tasks()
    new_id = 1 if len(tasks) == 0 else tasks[-1]["id"] + 1
    new_task = {
        "id": new_id,
        "task": body.task,
        "done": False,
        "notes": body.notes,
        "due_date": body.due_date
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task


@app.patch("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    save_tasks(new_tasks)
    return {"message": "Task deleted"}

@app.get("/tasks/search")
async def search_tasks(q: str):
    tasks = load_tasks()
    results = [t for t in tasks if q.lower() in t["task"].lower() or q.lower() in t["notes"].lower()]
    return results

@app.get("/tasks/overdue")
async def get_overdue():
    tasks = load_tasks()
    today = str(date.today())
    overdue = [t for t in tasks if t.get("due_date") and t["due_date"] < today and not t["done"]]
    return overdue

def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()