from typing import Optional, List

from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


reports = dict()
next_id = 1


class Report(BaseModel):
    problem1: Optional[str]
    problem2: Optional[str]
    problem3: Optional[str]
    place: Optional[str]
    school: Optional[str]
    city: Optional[str]
    workplace: Optional[str]
    id: Optional[int] = None


class Reports(BaseModel):
    reports: List[Report] = []


@app.post("/reports")
# def add_report(report: Report):
def add_report(problem1: Optional[str] = Form(...), problem2: Optional[str] = Form(...), problem3: Optional[str] = Form(...), place: Optional[str] = Form(...), school: Optional[str] = Form(...), city: str = Form(...), workplace: Optional[str] = Form(...)):
    global next_id

    report = Report()
    report.problem1 = problem1
    report.problem2 = problem2
    report.problem3 = problem3
    report.place = place
    report.school = school
    report.workplace = workplace

    report.id = next_id
    next_id += 1
    reports[report.id] = report
    return {"item_id": report.id}


@app.get("/reports", response_model=Reports)
def get_reports():
    result = Reports()
    if len(reports) > 0:
        result.reports = list(reports.values())
    else:
        result.reports = []
    return result


app.mount("/", StaticFiles(directory="static", html=True), name="static")
