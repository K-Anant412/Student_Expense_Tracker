import streamlit as st
from datetime import date
from calendar import month_name

MONTH_NAMES = [month_name[i] for i in range(1, 13)]
CURRENT_YEAR = date.today().year
YEARS = [CURRENT_YEAR - 2, CURRENT_YEAR - 1, CURRENT_YEAR, CURRENT_YEAR + 1]


def inject_custom_styles():
    st.markdown("""
    <style>
    /* Global Styles */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
        max-width: 1200px;
    }
    
    /* Card Styles */
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 12px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
    }
    .metric-title {
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #0F172A;
        font-size: 1.7rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .metric-subtext {
        color: #94A3B8;
        font-size: 0.8rem;
    }
    
    /* Status Badges */
    .badge-income {
        background-color: #DCFCE7;
        color: #15803D;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        display: inline-block;
    }
    .badge-expense {
        background-color: #FEE2E2;
        color: #B91C1C;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        display: inline-block;
    }
    .badge-normal {
        background-color: #DCFCE7;
        color: #15803D;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
    }
    .badge-warning {
        background-color: #FEF3C7;
        color: #B45309;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
    }
    .badge-danger {
        background-color: #FEE2E2;
        color: #B91C1C;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
    }
    
    /* Disclaimers & Notes */
    .disclaimer-box {
        background-color: #F1F5F9;
        border-left: 4px solid #3B82F6;
        padding: 10px 14px;
        border-radius: 4px;
        font-size: 0.82rem;
        color: #334155;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    
    /* Tables */
    div[data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
    }
    </style>
    """, unsafe_allow_html=True)


def format_inr(val):
    """Formats float/decimal into ₹ Indian Rupee format."""
    try:
        val = float(val or 0.0)
        return f"₹{val:,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"


def show_offline_banner():
    st.error("⚠️ **Flask REST API is Offline**")
    st.markdown("""
    The Streamlit frontend cannot establish an HTTP connection with the Flask backend API (`http://127.0.0.1:5000/api`).
    
    **How to fix:**
    1. Open a new terminal in the project directory.
    2. Start the Flask backend server:
       ```bash
       python app.py
       ```
    3. Once Flask starts, refresh this Streamlit page.
    """)
