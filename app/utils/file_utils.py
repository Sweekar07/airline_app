from datetime import datetime
import os, re
from collections import Counter
from typing import List, Dict
import pandas as pd
import plotly.express as px
from collections import defaultdict
from plotly.io import to_html
import plotly.graph_objects as go

OUTPUT_FOLDER = "app/output"

def generate_top_routes_chart(data):
    if not data:
        return "<p>No data available</p>"

    df_flights = pd.DataFrame([{
        "departure_iata": entry["departure"]["iata"],
        "arrival_iata": entry["arrival"]["iata"]
    } for entry in data if entry.get("departure") and entry.get("arrival")])

    if df_flights.empty:
        return "<p>No valid flight data</p>"

    route_counts = defaultdict(int)
    for _, row in df_flights.iterrows():
        route = f"{row['departure_iata']} → {row['arrival_iata']}"
        route_counts[route] += 1

    df_routes = pd.DataFrame(list(route_counts.items()), columns=["Route", "Count"])
    df_routes = df_routes.sort_values(by="Count", ascending=False)

    fig = px.bar(df_routes, x="Route", y="Count", title="Popular Routes (All)", color_discrete_sequence=["skyblue"])
    fig.update_layout(
        xaxis_title="Route",
        yaxis_title="Flight Count",
        xaxis_tickangle=-45
    )
    return to_html(fig, include_plotlyjs="cdn", full_html=False)

def generate_demand_period_chart(data):
    if not data:
        return "<p>No data available</p>"

    df_flights = pd.DataFrame([{
        "departure_time": entry["departure"]["scheduled"]
    } for entry in data if entry.get("departure") and entry["departure"].get("scheduled")])

    if df_flights.empty:
        return "<p>No valid departure times</p>"

    df_flights["departure_hour"] = pd.to_datetime(df_flights["departure_time"]).dt.hour
    demand_periods = df_flights["departure_hour"].value_counts().sort_index()

    fig_bar = px.bar(
        x=demand_periods.index,
        y=demand_periods.values,
        title="High-Demand Periods (Bar Chart)"
    )
    fig_bar.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Number of Flights"
    )
    fig_bar.update_traces(
        marker_color='rgb(158,185,243)',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5,
        opacity=0.6
    )

    return to_html(fig_bar, include_plotlyjs=False, full_html=False)

def list_available_dates():
    dates = set()
    pattern = re.compile(r"flights_(\d{4}-\d{2}-\d{2})_")

    if not os.path.exists(OUTPUT_FOLDER):
        return []

    for file in os.listdir(OUTPUT_FOLDER):
        match = pattern.match(file)
        if match:
            dates.add(match.group(1))

    return sorted(list(dates))

def process_flight_data(data: List[Dict]):
    routes = []
    airlines = []
    departure_hours = []
    origins = []
    destinations = []

    for f in data:
        if not f.get("departure") or not f.get("arrival"):
            continue
        routes.append(f"{f['departure']['airport']} → {f['arrival']['airport']}")
        if f.get("airline") and f["airline"].get("name"):
            airlines.append(f["airline"]["name"])
        if f["departure"].get("scheduled"):
            try:
                hour = datetime.fromisoformat(f["departure"]["scheduled"]).hour
                departure_hours.append(hour)
            except Exception:
                pass
        if f["departure"].get("airport"):
            origins.append(f["departure"]["airport"])
        if f["arrival"].get("airport"):
            destinations.append(f["arrival"]["airport"])

    route_counts = Counter(routes)
    hour_counts = Counter(departure_hours)
    airline_counts = Counter(airlines)
    origin_counts = Counter(origins)
    destination_counts = Counter(destinations)

    return {
        "top_routes": route_counts.most_common(),  # show all if needed
        "total_flights": len(data),
        "most_common_route": route_counts.most_common(1)[0] if route_counts else None,
        "peak_hour": hour_counts.most_common(1)[0] if hour_counts else None,
        "top_airline": airline_counts.most_common(1)[0] if airline_counts else None,
        "top_origin": origin_counts.most_common(1)[0] if origin_counts else None,
        "top_destination": destination_counts.most_common(1)[0] if destination_counts else None
    }

def generate_airline_activity_chart(data):
    if not data:
        return "<p>No data available</p>"

    df_flights = pd.DataFrame([
        {"airline_name": entry["airline"]["name"]}
        for entry in data
        if entry.get("airline") and entry["airline"].get("name")
    ])

    if df_flights.empty:
        return "<p>No valid airline data</p>"

    airline_counts = df_flights["airline_name"].value_counts()

    fig3 = px.bar(
        x=airline_counts.index,
        y=airline_counts.values,
        title="Airline Activity",
        labels={"x": "Airline", "y": "Number of Flights"},
        color_discrete_sequence=["#3399FF"]
    )
    fig3.update_layout(
        xaxis_title="Airline",
        yaxis_title="Number of Flights"
    )

    return to_html(fig3, include_plotlyjs=False, full_html=False)
