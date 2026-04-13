# FastAPI Task Manager

Simple REST API for managing tasks using FastAPI and a JSON file.

## Requirements

* Python 3.8+
* fastapi
* uvicorn

## Install

```bash
pip install fastapi uvicorn
```

## Run

```bash
uvicorn main:app --reload
```

## Endpoints

* GET /tasks
* POST /tasks
* PATCH /tasks/{task_id}/complete
* DELETE /tasks/{task_id}
* GET /tasks/search?q=keyword
* GET /tasks/overdue

## Notes

* Data is stored in `tasks.json`
* Due dates should be in `YYYY-MM-DD` format

## quick note
i forgot to create the repo so hackatime only shows 1 hour (i have 2 in reality) :3
