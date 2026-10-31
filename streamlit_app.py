import streamlit as st
from frontend_services.api_client import APIClient
from frontend_views.ui_common import inject_custom_styles, format_inr
from frontend_views.dashboard import render_dashboard_view
from frontend_views.transactions import render_transactions_view
from frontend_views.add_transaction import render_add_transaction_view
from frontend_views.budgets import render_budgets_view
from frontend_views.analytics import render_analytics_view
from frontend_views.categories import render_categories_view
from frontend_views.reports import render_reports_view
from frontend_views.about import render_about_view

# Configure page settings
st.set_page_config(
    page_title="Student Expense Tracker & Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom UI styling
inject_custom_styles()


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding-bottom: 12px; border-bottom: 1px solid #E2E8F0; margin-bottom: 16px;">
            <div style="font-size: 2.2rem;">💰</div>
            <h2 style="margin: 0; font-size: 1.25rem; color: #1E293B;">Student Expense Tracker</h2>
            <p style="margin: 2px 0 0 0; font-size: 0.8rem; color: #64748B;">Personal Finance & Budget Analyzer</p>
        </div>
        """, unsafe_allow_html=True)

        # Health Check Status Indicator
        health = APIClient.check_health()
        if health["ok"]:
            st.success("🟢 **Flask API:** Connected (`:5000`)")
        else:
            st.error("🔴 **Flask API:** Offline (`:5000`)")

        st.markdown("### Navigation")
        nav_choice = st.radio(
            "Go to",
            [
                "📊 Dashboard",
                "💳 Transactions",
                "➕ Add Transaction",
                "🎯 Monthly Budgets",
                "📈 Spending Analytics",
                "🏷️ Categories",
                "📄 Reports & CSV Export",
                "ℹ️ About Project"
            ],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.75rem; color: #94A3B8; text-align: center;">
            Student Expense Tracker & Analyzer<br>
            BCA Academic Project 2026-27<br>
            Shivaji University, Kolhapur
        </div>
        """, unsafe_allow_html=True)

        return nav_choice


def main():
    nav = render_sidebar()

    if nav == "📊 Dashboard":
        render_dashboard_view()
    elif nav == "💳 Transactions":
        render_transactions_view()
    elif nav == "➕ Add Transaction":
        render_add_transaction_view()
    elif nav == "🎯 Monthly Budgets":
        render_budgets_view()
    elif nav == "📈 Spending Analytics":
        render_analytics_view()
    elif nav == "🏷️ Categories":
        render_categories_view()
    elif nav == "📄 Reports & CSV Export":
        render_reports_view()
    elif nav == "ℹ️ About Project":
        render_about_view()


if __name__ == "__main__":
    main()
