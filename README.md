# ✈️ Airline Booking Demand Dashboard

A modern Python web application that fetches, processes, and visualizes airline booking market demand data. It helps analyze popular routes, peak flight times, top airlines, and more using interactive charts.

---

## 🚀 Features

- 🔍 **Flight Data Fetching** from [AviationStack API](https://aviationstack.com/)
- 🧠 **Insights Dashboard** with:
  - Top routes
  - Peak demand periods
  - Most active airlines and airports
- 📦 **Local Caching** to avoid exceeding API request limits
- 📅 **Date Filtering** (cached and custom)
- 📈 **Interactive Visualizations** using Plotly
- 💡 **Info Cards** showing key stats
- ❌ **Error Handling** with a custom error page

---

## 🛠️ Tech Stack

| Technology    | Use Case                             |
|---------------|---------------------------------------|
| **FastAPI**   | Web framework & routing               |
| **Jinja2**    | HTML templating                       |
| **Plotly.js** | Interactive graphs in the browser     |
| **Pandas**    | Data processing & aggregation         |
| **Python-dotenv** | Environment variable management  |

---

## 📂 Project Structure

```
app/
│
├── templates/
│ ├── dashboard.html # Main UI template
│ └── error.html # Error fallback page
│
├── utils/
│ └── file_utils.py # Data processing and chart utilities
│
├── services/
│ └── aviationstack_service.py # Fetching from AviationStack API
│
├── output/ # Cached flight data by date
│
└── main.py # FastAPI entrypoint
```

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Sweekar07/airline_app.git
cd airline_app
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Configure .env
Create a .env file in the root directory:

```
AVIVATION_STACK_API_KEY=your_api_key_here
```

 ### Run the app
 ```
uvicorn main:app --reload
```

Then visit: http://localhost:8000


#### 📌 Notes

API has a 100 requests/month limit, so the app caches results in the output/ folder.

Only data for the last 3 months is supported for filtering.
