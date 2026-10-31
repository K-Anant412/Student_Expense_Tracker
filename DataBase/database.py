import os
import pymysql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

DEFAULT_CATEGORIES = [
    # Expense Categories
    {"name": "Food", "type": "Expense", "description": "Meals, snacks, dining hall, and cafeteria groceries"},
    {"name": "Transport", "type": "Expense", "description": "Bus, metro, auto, fuel, and travel tickets"},
    {"name": "Education", "type": "Expense", "description": "Books, tuition, stationery, courses, and exam fees"},
    {"name": "Accommodation", "type": "Expense", "description": "Hostel fees, PG rent, maintenance, and laundry"},
    {"name": "Shopping", "type": "Expense", "description": "Clothing, personal care, electronics, and accessories"},
    {"name": "Entertainment", "type": "Expense", "description": "Movies, outings, subscriptions, and events"},
    {"name": "Healthcare", "type": "Expense", "description": "Medicines, doctor visits, and health wellness"},
    {"name": "Bills", "type": "Expense", "description": "Mobile recharges, internet bills, and utilities"},
    {"name": "Other", "type": "Expense", "description": "Miscellaneous and unplanned student expenses"},
    # Income Categories
    {"name": "Allowance", "type": "Income", "description": "Monthly pocket money or allowance from parents"},
    {"name": "Scholarship", "type": "Income", "description": "College merit, government, or institutional scholarships"},
    {"name": "Part-time Work", "type": "Income", "description": "Income earned from campus or local part-time jobs"},
    {"name": "Freelancing", "type": "Income", "description": "Design, coding, tutoring, or online client gigs"},
    {"name": "Gift", "type": "Income", "description": "Monetary gifts from family and friends"},
    {"name": "Other", "type": "Income", "description": "Other miscellaneous income sources"},
]


def ensure_database_exists():
    """
    Connects to MySQL server without selecting a database and creates
    the application database if it does not already exist.
    """
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    port = int(os.getenv("DB_PORT", 3306))
    db_name = os.getenv("DB_NAME", "student_expense_tracker")

    try:
        conn = pymysql.connect(host=host, user=user, password=password, port=port)
        with conn.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
        conn.commit()
        conn.close()
        print(f"[DB] Database `{db_name}` verified or created successfully.")
    except Exception as e:
        print(f"[DB WARN] Failed to verify/create database `{db_name}`: {e}")


def seed_default_categories():
    """
    Seeds standard student income and expense categories if they do not already exist.
    """
    from Modules.models import Category, User

    # Ensure a default student profile exists
    default_user = User.query.filter_by(id=1).first()
    if not default_user:
        default_user = User(
            id=1,
            username="student_scholar",
            email="student@college.edu",
            full_name="College Student",
            college_name="Shri Shahaji Chhatrapati Mahavidyalaya, Kolhapur",
            currency="₹",
        )
        db.session.add(default_user)
        try:
            db.session.commit()
            print("[DB] Default student profile initialized.")
        except Exception:
            db.session.rollback()

    # Seed default categories
    existing_categories = {(c.name.strip().lower(), c.type) for c in Category.query.all()}
    added_count = 0
    for cat_data in DEFAULT_CATEGORIES:
        key = (cat_data["name"].strip().lower(), cat_data["type"])
        if key not in existing_categories:
            new_cat = Category(
                name=cat_data["name"],
                type=cat_data["type"],
                description=cat_data["description"],
                is_default=True,
            )
            db.session.add(new_cat)
            added_count += 1

    if added_count > 0:
        try:
            db.session.commit()
            print(f"[DB] Seeded {added_count} default categories.")
        except Exception as e:
            db.session.rollback()
            print(f"[DB ERROR] Error seeding default categories: {e}")


def init_db(app):
    """
    Full database initialization:
    1. Ensures MySQL database exists
    2. Initializes Flask-SQLAlchemy with app
    3. Creates tables if not present
    4. Seeds default categories
    """
    ensure_database_exists()
    db.init_app(app)

    with app.app_context():
        try:
            # Verify connectivity
            db.session.execute(text("SELECT 1"))
            db.create_all()
            print("[DB SUCCESS] MySQL connection verified and tables created.")
            seed_default_categories()
        except Exception as e:
            print(f"[DB ERROR] Failed during table creation or seeding: {e}")
            raise e
