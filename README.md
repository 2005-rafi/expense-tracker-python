# Expense Tracker

A **full-stack expense tracker application** built entirely in Python, featuring a user-friendly Streamlit interface and a robust Django backend, leveraging SQLite as the database. The application enables complete CRUD operations, budget management, monthly expense visualizations, and seamless cross-platform deployment, with one-click launching via a batch script.

## Features

- Intuitive Streamlit frontend for tracking expenses, editing entries, managing categories, and displaying monthly summaries
- Django REST API backend supporting CRUD operations, monthly aggregations, and data resets
- SQLite as the default database (no external database setup required)
- Rich data visualizations: line charts, bar graphs, and pie charts for monthly analytics
- Simple batch script (`setup.bat`) to launch frontend and backend servers simultaneously
- Dark theme interface and budget settings for improved usability

## Getting Started

Follow these instructions to set up, run, and use the Expense Tracker application locally.

### Prerequisites

- Python 3.8 or higher
- Windows operating system (batch script provided; for Mac/Linux, run commands manually)
- Recommended: Git for code management

### Installation

1. **Clone the repository:**

git clone https://github.com/yourusername/expense-tracker.git

cd expense-tracker

2. **Install required Python packages:**

pip install -r requirements.txt

**Dependencies included:**
- Django
- Django REST Framework
- django-cors-headers
- Streamlit
- pymongo (for optional MongoDB fallback)
- requests
- plotly
- pandas

### Running the Application

#### Using the Batch Script (Windows)

Simply run the provided batch file: setup.bat

This launches both the Django backend (port 8000) and the Streamlit frontend (port 8501) in separate terminal windows.

- Backend: http://localhost:8000
- Frontend: http://localhost:8501

#### Manual Startup (Mac/Linux or CLI):

Open two terminal windows.
- **Terminal 1 (backend):** python backend.py

- **Terminal 2 (frontend):** streamlit run frontend.py

  
Ensure both are running before accessing the dashboard in your browser.

### Project Structure

| File/Folders         | Description                                               |
|----------------------|----------------------------------------------------------|
| `frontend.py`        | Streamlit user interface (dashboard, forms, charts)      |
| `backend.py`         | Django REST API server (CRUD, aggregation endpoints)     |
| `db.py`              | Database handling (SQLite, and optional MongoDB support) |
| `settings_config.py` | Django & DB configuration routine                        |
| `run.py`             | Launches backend & frontend together (programmatically)  |
| `requirements.txt`   | List of Python dependencies                              |
| `setup.bat`          | Windows batch script for easy launch                     |
| `instructions.txt`   | Brief user instructions                                  |

### Usage Instructions

- **Add/Edit Expenses:** Use the sidebar and main form to enter details (product, amount, category). Expenses can be edited or deleted via buttons.
- **Set Budget:** Adjust your monthly budget at any time using the sidebar.
- **View Summaries:** Switch between months to see detailed breakdowns, visualizations, and remaining budgets.
- **Data Reset:** Click "Reset All Expenses" to clear all records.
- **Visual Analytics:** Access line, bar, and pie charts generated for active month summaries.

### API Endpoints (Backend)

Common endpoints (available at `http://localhost:8000/api/`):

| Endpoint                   | Method   | Function                       |
|----------------------------|----------|--------------------------------|
| `api/expenses`             | GET      | Get all expenses               |
| `api/expenses/add`         | POST     | Add new expense                |
| `api/expenses/<id>/update` | PUT      | Update expense by ID           |
| `api/expenses/<id>/delete` | DELETE   | Delete expense by ID           |
| `api/expenses/reset`       | DELETE   | Delete all expenses            |
| `api/expenses/total`       | GET      | Get the sum of all expenses    |
| `api/health`               | GET      | Health check                   |

### Customization

- To change backend settings (port, DB name), edit `settings_config.py`.
- Categories can be modified in the frontend UI as required.

### Troubleshooting

- If connection errors occur, confirm both backend and frontend servers are running.
- If `setup.bat` fails on your platform, launch via manual method above.
- For Python package errors, run `pip install -r requirements.txt` again.

### License

This project is released under the MIT License.

### Contributors

- Maintainer: [Your Name]
- For questions or contributions, please submit issues or pull requests via GitHub.

---

**Enjoy using Expense Tracker! For feedback or suggestions, open an issue in the repository.**
