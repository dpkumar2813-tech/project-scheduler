import json, sqlite3
from pathlib import Path
from datetime import date
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from scheduler import schedule

app = FastAPI(title='Project Scheduler API')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173','http://127.0.0.1:5173'], allow_methods=['*'], allow_headers=['*'])
DB = Path(__file__).with_name('projects.db')
def connection():
    con = sqlite3.connect(DB)
    con.execute('CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, data TEXT NOT NULL)')
    return con
class Task(BaseModel):
    id: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=150)
    owner: str = Field(default='', max_length=100)
    duration: int = Field(ge=1, le=1000)
    dependencies: list[str] = Field(default_factory=list)
class Project(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    start_date: date
    holidays: list[date] = Field(default_factory=list)
    tasks: list[Task] = Field(default_factory=list, max_length=200)
    baseline: dict[str, str] = Field(default_factory=dict)
def calculate(p):
    try: return schedule([t.model_dump() for t in p.tasks], p.start_date.isoformat(), [d.isoformat() for d in p.holidays])
    except ValueError as e: raise HTTPException(422, str(e))
@app.get('/api/health')
def health(): return {'status':'ok'}
@app.post('/api/schedule')
def preview(p: Project): return calculate(p)
@app.get('/api/projects')
def projects():
    with connection() as con: return [{'id': row[0], **json.loads(row[1])} for row in con.execute('SELECT id,data FROM projects ORDER BY id DESC')]
@app.post('/api/projects')
def create(p: Project):
    calculate(p)
    with connection() as con:
        cursor = con.execute('INSERT INTO projects(data) VALUES (?)', (p.model_dump_json(),))
        return {'id':cursor.lastrowid}
@app.put('/api/projects/{key}')
def update(key: int, p: Project):
    calculate(p)
    with connection() as con:
        cursor = con.execute('UPDATE projects SET data=? WHERE id=?', (p.model_dump_json(), key))
        if not cursor.rowcount: raise HTTPException(404,'Project not found')
    return {'id':key}
@app.delete('/api/projects/{key}')
def delete(key: int):
    with connection() as con:
        cursor = con.execute('DELETE FROM projects WHERE id=?',(key,))
        if not cursor.rowcount: raise HTTPException(404,'Project not found')
    return {'deleted':True}
