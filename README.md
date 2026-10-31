# Student Expense Tracker and Analyzer

A full-stack, local personal finance management and budget analysis system engineered specifically for college students. The application records income inflows and expense outflows, categorizes transactions, enforces monthly category budgets, visualizes financial spending patterns with interactive analytical charts, and exports detailed CSV financial reports.

---

## 🏛️ System Architecture

The project implements a decoupled 3-tier client-server architecture:

```
[ Streamlit Web UI ] (Port 8501)
         │  HTTP JSON REST Requests
         ▼
[ Flask REST API ] (Port 5000)
         │
   [ Services / Logic Layer ]
   ├── Transaction Service
   ├── Category Service
   ├── Budget Calculation Engine
   └── Analytics & Reporting Engine
         │  SQLAlchemy ORM / PyMySQL
         ▼
[ MySQL Relational Database ] (Port 3306)
   Database: `student_expense_tracker`
```

- **Frontend Interface (Streamlit)**: User-facing dashboard, responsive transaction tables, category budget progress monitors, interactive Altair charts, and CSV report export.
- **Backend API (Flask)**: RESTful API handling input validation, business logic, financial calculations, and secure database transactions.
- **Relational Persistence (MySQL)**: Normalized relational schema (`users`, `categories`, `transactions`, `budgets`) with foreign keys, decimal precision, and indexes.

---

## 🚀 Key Functional Modules

1. **📊 Financial Dashboard**:
   - Total Income, Total Expenses, and Net Recorded Balance for the selected month.
   - Overall monthly category budget utilization percentage.
   - Highest-spending expense category and transaction volume.
   - Visual 6-month Income vs. Expenses comparison and category distribution charts.
   - Real-time budget warning alerts when spending approaches (≥80%) or exceeds configured limits.
   - Explicit disclaimer that net recorded balance tracks entered transactions and is not linked to a bank account.

2. **💳 Transaction Management**:
   - Complete CRUD operations: Record, view, edit, search, filter, and delete transactions.
   - Strict server-side validation: Positive amounts (> 0), valid date, valid transaction type (`Income` / `Expense`), and matching category.
   - Search by keyword (description, category, payment method).
   - Filter by date range, transaction type, and category.
   - Sorting by date or amount in ascending or descending order.

3. **🎯 Monthly Category Budget Management**:
   - Set monthly spending caps for individual expense categories (e.g., Food: ₹3,500, Transport: ₹1,200).
   - Real-time expense computation against category budgets for the specified calendar month and year.
   - Utilization percentage calculation and remaining budget computation.
   - Configurable alert threshold (default 80%) with visual status indicators: *Within Limit* (Green), *Approaching Limit* (Yellow/Warning), and *Exceeded* (Red/Danger).
   - Enforces unique category budgets per month/year (prevents duplicate budgets).

4. **📈 Advanced Spending Analytics**:
   - 12-Month historical trend of income, expenses, and net student savings.
   - Expense distribution by category with percentage breakdowns.
   - Ranked list of top spending categories.
   - Month-over-month comparison calculating exact expense/income changes against the previous calendar month.
   - Average monthly expenses over active recording periods.

5. **🏷️ Category System Management**:
   - Pre-seeded standard student categories (Food, Transport, Education, Accommodation, Shopping, Entertainment, Healthcare, Bills, Allowance, Scholarship, Freelancing, etc.).
   - Create custom categories with unique names per type.
   - Safe deletion protection preventing removal of categories associated with existing transactions or active budgets.

6. **📄 Financial Statement & CSV Export**:
   - Summary statement displaying reporting period, total inflows, total outflows, and net recorded balance.
   - Filterable detailed transaction records.
   - Official CSV export with standardized column headers ready for college submission or personal record-keeping.

7. **🧪 Academic Demonstration Utilities**:
   - One-click demo data seeder loading realistic student financial transactions across multiple months and configured budgets for college demonstration.
   - Clean slate reset function to clear records for fresh student testing without dropping database tables.

---

## 💻 Tech Stack & Requirements

- **Programming Language**: Python 3.10+
- **Backend Framework**: Flask 3.x, Flask-CORS, Flask-SQLAlchemy 3.x
- **Frontend Framework**: Streamlit 1.30+
- **Database Engine**: MySQL Server 8.0+ / MariaDB
- **Database Driver**: PyMySQL / SQLAlchemy
- **Data Analysis**: Pandas
- **Visualization**: Altair & Streamlit Native Charts
- **Testing**: Pytest

---

## ⚙️ Installation and Setup Guide

### 1. Prerequisites
Ensure you have Python installed and MySQL running locally on port 3306.

### 2. Configure Environment Variables
Copy the sample environment file to `.env`:
```bash
cp env.example .env
```
Edit `.env` to match your local MySQL credentials:
```env
FLASK_ENV=development
SECRET_KEY=student-expense-tracker-secret-2026
PORT=5000
API_BASE_URL=http://127.0.0.1:5000/api

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=student_expense_tracker
DB_PORT=3306
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database & Seed Categories
Run the automated database initialization script. This creates the `student_expense_tracker` database, generates all relational tables, and seeds standard default categories:
```bash
python DataBase/init_db.py
```
*(Optional)* To populate realistic academic demonstration data immediately:
```bash
python DataBase/init_db.py --seed-demo
```

---

## 🏃 Running the Application

### Option A: Concurrent Multi-Service Launcher (Recommended)
You can launch both Flask Backend and Streamlit Frontend concurrently with a single command:
```bash
python run.py
```

### Option B: Separate Terminals

**Terminal 1 - Flask REST API Backend:**
```bash
python app.py
```
*API will run at:* `http://127.0.0.1:5000`  
*Health check:* `http://127.0.0.1:5000/api/health`

**Terminal 2 - Streamlit Web UI Frontend:**
```bash
streamlit run streamlit_app.py
```
*Streamlit UI will run at:* `http://localhost:8501`

---

## 🧪 Automated Testing

Execute the comprehensive automated test suite with pytest:
```bash
python -m pytest -v
```

The test suite validates:
- API health check and database connectivity.
- Pre-seeded default categories.
- Transaction validation (positive amount > 0, date validation, type matching).
- Transaction CRUD lifecycle (Create, Read, Update, Delete, 404 handling).
- Budget duplicate prevention and boundary handling.
- Benchmark financial calculations:
  - Recorded Income: ₹10,000.00
  - Recorded Expenses: ₹4,000.00
  - Net Recorded Balance: ₹6,000.00
  - Category Budget: ₹5,000.00
  - Category Expenses: ₹4,000.00
  - Budget Utilization: 80.0%
  - Remaining Category Budget: ₹1,000.00
- Safe division by zero prevention when budget is zero.

---

## 📁 Project Directory Structure

```
S_Expense_Tracker/
├── .streamlit/
│   └── config.toml             # Streamlit visual theme and server settings
├── assets/                     # Captured UI application screenshots
│   ├── dashboard.png
│   ├── transactions.png
│   ├── add_transaction.png
│   ├── monthly_budgets.png
│   ├── spending_analytics.png
│   └── reports_csv_export.png
├── DataBase/
│   ├── database.py             # Database connection, seeder, and setup
│   ├── init_db.py              # CLI database initialization and seed script
│   └── schema.sql              # Normalized MySQL relational schema DDL
├── frontend_services/
│   └── api_client.py           # HTTP Requests client connecting UI to Flask
├── frontend_views/
│   ├── __init__.py
│   ├── ui_common.py            # Styling tokens, currency formatters, offline banner
│   ├── dashboard.py            # Financial dashboard view
│   ├── transactions.py         # Transaction history, search, edit, delete view
│   ├── add_transaction.py      # Transaction entry form with dynamic category dropdown
│   ├── budgets.py              # Monthly category budget management view
│   ├── analytics.py            # Spending analytics, trends, rankings, comparison
│   ├── categories.py           # Category listing, creation, and safe deletion
│   ├── reports.py              # Financial summary statement and CSV export
│   └── about.py                # Academic project metadata and demo data controls
├── Modules/
│   └── models.py               # SQLAlchemy models (User, Category, Transaction, Budget)
├── Routes/
│   ├── transaction_route.py    # /api/transactions REST API endpoints
│   ├── category_route.py       # /api/categories REST API endpoints
│   ├── budget_route.py         # /api/budgets REST API endpoints
│   └── analytics_route.py      # /api/dashboard, /api/analytics, /api/reports endpoints
├── Services/
│   ├── transaction_service.py  # Transaction CRUD and filtering business logic
│   ├── category_service.py     # Category business logic and safe deletion validation
│   ├── budget_service.py       # Monthly budget tracking and alert calculation
│   ├── analytics_service.py    # Financial metrics, multi-month trends, comparison
│   └── demo_data_service.py    # Academic demonstration records loader
├── tests/
│   ├── test_api_endpoints.py   # Pytest suite for REST endpoints and DB integration
│   └── test_calculations.py    # Pytest suite for benchmark financial formulas
├── Utils/
│   └── helpers.py              # Validation, INR formatting, and standard JSON responses
├── .env                        # Local database credentials (ignored in git)
├── env.example                 # Environment variable template
├── .gitignore                  # Git ignore rules
├── app.py                      # Flask REST API entry point
├── app_ui.py                   # Streamlit runner alias wrapper
├── config.py                   # Centralized configuration loader
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── run.py                      # Multi-service launcher script
└── streamlit_app.py            # Main Streamlit user interface entry point
```

---
