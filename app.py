from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os

app = FastAPI(title="CleanSmart Inspections v1")

# Set up templates and static folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Create a simple in-memory list to hold “reports” for now
reports = []

# Mount static folder (even if empty for now)
if not os.path.exists(os.path.join(BASE_DIR, "static")):
    os.makedirs(os.path.join(BASE_DIR, "static"), exist_ok=True)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Simple dashboard listing all reports
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "reports": reports,
            "title": "CleanSmart Inspections – Dashboard",
        },
    )


@app.get("/new", response_class=HTMLResponse)
async def new_report_form(request: Request):
    # Simple form to create a “report”
    return templates.TemplateResponse(
        "new.html",
        {
            "request": request,
            "title": "New Inspection Report",
        },
    )


@app.post("/new", response_class=HTMLResponse)
async def create_report(
    request: Request,
    client_name: str = Form(...),
    property_address: str = Form(...),
    report_type: str = Form(...),
    notes: str = Form(""),
):
    report = {
        "id": len(reports) + 1,
        "client_name": client_name,
        "property_address": property_address,
        "report_type": report_type,
        "notes": notes,
    }
    reports.append(report)
    return templates.TemplateResponse(
        "created.html",
        {
            "request": request,
            "report": report,
            "title": "Report Created",
        },
    )
