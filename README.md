# Planwise — Project Scheduler with Critical-Path Gantt

A React + FastAPI project planning application with persistent SQLite storage.

## Windows: start in two terminals
Install Python 3.10+ and Node.js 20.19+ or 22.12+. Node 24 also works.
Extract the ZIP into a NEW folder; do not overwrite your earlier work.
Open the extracted project-scheduler folder in VS Code.

Terminal 1 (PowerShell):
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Leave this terminal running. No PowerShell activation or execution-policy change is needed.

Terminal 2 (Terminal > New Terminal, from project-scheduler root):
```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```
Open http://localhost:5173. Leave both terminals running.
API documentation: http://127.0.0.1:8000/docs.

## Using the app
The example website project loads initially. Save it to retain it after restart.
Use Add task to enter a name, owner, integer working-day duration, and predecessors.
Use Task list to edit or delete tasks. Dates recalculate automatically.
Capture baseline stores each task's current finish date; save afterward.
Saved projects appear in the sidebar. The + button starts an empty project.
Holidays must be comma-separated YYYY-MM-DD dates; click outside the field to apply.
CSV exports scheduled dates, critical status, and slack.

## Scheduling model
Directed acyclic graph, depth-first topological ordering and cycle detection.
Forward pass computes earliest start/finish; backward pass computes latest start/finish.
Slack = latest start − earliest start. Every zero-slack task is highlighted; multiple critical paths are possible.
Dependencies are finish-to-start with zero lag. Dates are inclusive; duration uses Monday–Friday working days excluding holidays.
Owner workload shows summed effort, not resource-constrained scheduling.

## Structure
frontend/src/App.jsx — UI, task editor, timeline SVG, API requests
frontend/src/style.css — responsive styling
backend/main.py — validated REST API and parameterized SQLite queries
backend/scheduler.py — graph and critical-path calculations
backend/tests/test_scheduler.py — scheduling tests

## Tests
From backend:
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
From frontend:
```powershell
npm.cmd run build
```

## Scope and next steps
Local single-user MVP. No login, authorization, payment, or production hosting is included.
SQLite is intentional for easy startup; PostgreSQL integration is a future extension.
No drag-to-resize, PNG export, or calendar export is implemented.
A baseline displays previous finish dates below bars; it is not a separate overlay bar.
Add authentication, database migrations, PostgreSQL, owner conflict detection and deployment before public multi-user use.
Never claim unimplemented features or invented performance metrics on your resume.

Suggested resume statement after running and understanding it:
Built a full-stack project scheduler using React, FastAPI and SQLite; implemented dependency validation, topological scheduling, critical-path analysis, working-day calendars and interactive SVG Gantt visualization.
