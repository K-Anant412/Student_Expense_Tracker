"""
Database Initialization Script for Student Expense Tracker and Analyzer.
Run this script directly to verify database tables, seed default categories,
or optionally load realistic demonstration data.

Usage:
    python DataBase/init_db.py             # Verify tables and seed default categories
    python DataBase/init_db.py --seed-demo # Also loads realistic student demonstration records
    python DataBase/init_db.py --clear     # Clears transactions and budgets for a fresh slate
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from DataBase.database import seed_default_categories
from Services.demo_data_service import seed_demo_data, clear_demo_data

def main():
    with app.app_context():
        if "--clear" in sys.argv:
            print("[INFO] Clearing transactions and budgets...")
            success, msg = clear_demo_data()
            print(f"[RESULT] {msg}")
            return

        print("[INFO] Ensuring default categories are seeded...")
        seed_default_categories()

        if "--seed-demo" in sys.argv:
            print("[INFO] Seeding realistic demonstration data...")
            success, msg = seed_demo_data(force=True)
            print(f"[RESULT] {msg}")

        print("[SUCCESS] Database initialization completed successfully.")

if __name__ == "__main__":
    main()
