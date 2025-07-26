from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.aviationstack_service import get_flight_data
from app.utils.file_utils import (
    process_flight_data, 
    list_available_dates, generate_airline_activity_chart,
    generate_top_routes_chart, generate_demand_period_chart
)
import os

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, cached_date: str = None, custom_date: str = None):
    try:
        # Generate available cached dates (from output folder)
        output_dir = "app/output"
        available_dates = sorted(
            [f.replace(".json", "") for f in os.listdir(output_dir) if f.endswith(".json")]
        )
        available_dates = list_available_dates()

        date = custom_date or cached_date or available_dates[-1]
        data = await get_flight_data(date)
        insights = process_flight_data(data)
        chart_top_routes_html = generate_top_routes_chart(data)
        chart_demand_html  = generate_demand_period_chart(data)
        chart_airline_html = generate_airline_activity_chart(data)

        # Define min/max for custom date input (past 3 months only)
        today = datetime.today().date()
        max_date = today
        min_date = today - timedelta(days=90)

        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "insights": insights,
            "date": date,
            "available_dates": available_dates,
            "chart_top_routes_html": chart_top_routes_html,
            "chart_demand_html": chart_demand_html,
            "chart_airline_html": chart_airline_html,
            "min_date": min_date.isoformat(),
            "max_date": max_date.isoformat(),
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": str(e),
            "date": custom_date or cached_date or "Unknown"
        })
