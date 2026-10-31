import streamlit as st
import pandas as pd
from datetime import date
from calendar import month_name
from frontend_services.api_client import APIClient
from frontend_views.ui_common import format_inr, show_offline_banner, MONTH_NAMES, YEARS


def render_dashboard_view():
    st.title("📊 Student Financial Dashboard")
    st.caption("Real-time summary of recorded student income, expenses, and category budgets.")

    today = date.today()

    # Filter Bar
    f_col1, f_col2, f_col3 = st.columns([2, 2, 4])
    with f_col1:
        selected_month_name = st.selectbox("Select Month", MONTH_NAMES, index=today.month - 1, key="dash_month")
        selected_month = MONTH_NAMES.index(selected_month_name) + 1
    with f_col2:
        selected_year = st.selectbox("Select Year", YEARS, index=YEARS.index(today.year) if today.year in YEARS else 2, key="dash_year")
    with f_col3:
        st.write("")
        st.write("")
        if st.button("🔄 Refresh Data", key="refresh_dash"):
            st.rerun()

    # Fetch data from Flask API
    with st.spinner("Retrieving financial records from Flask backend..."):
        resp = APIClient.get_dashboard(month=selected_month, year=selected_year)

    if not resp["ok"]:
        show_offline_banner()
        return

    data = resp["data"]
    total_income = data.get("total_income", 0.0)
    total_expenses = data.get("total_expenses", 0.0)
    net_balance = data.get("net_balance", 0.0)
    budget_utilization = data.get("budget_utilization", 0.0)
    total_budget = data.get("total_budget", 0.0)
    trans_count = data.get("transaction_count", 0)
    top_cat = data.get("highest_spending_category", {})

    # Top KPI Metrics Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #10B981;">
            <div class="metric-title">Total Income</div>
            <div class="metric-value" style="color: #059669;">{format_inr(total_income)}</div>
            <div class="metric-subtext">Received in {selected_month_name} {selected_year}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #EF4444;">
            <div class="metric-title">Total Expenses</div>
            <div class="metric-value" style="color: #DC2626;">{format_inr(total_expenses)}</div>
            <div class="metric-subtext">Spent in {selected_month_name} {selected_year}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        bal_color = "#2563EB" if net_balance >= 0 else "#DC2626"
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #2563EB;">
            <div class="metric-title">Net Recorded Balance</div>
            <div class="metric-value" style="color: {bal_color};">{format_inr(net_balance)}</div>
            <div class="metric-subtext">Income minus expenses</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #8B5CF6;">
            <div class="metric-title">Budget Utilization</div>
            <div class="metric-value" style="color: #7C3AED;">{budget_utilization}%</div>
            <div class="metric-subtext">Budget: {format_inr(total_budget)}</div>
        </div>
        """, unsafe_allow_html=True)

    # Secondary row of metrics
    s1, s2 = st.columns(2)
    with s1:
        top_name = top_cat.get("name", "None")
        top_amt = format_inr(top_cat.get("amount", 0.0))
        st.info(f"🏆 **Highest-Spending Category:** **{top_name}** ({top_amt})")
    with s2:
        st.info(f"📝 **Recorded Transactions in Period:** **{trans_count}** transaction(s)")

    # Bank account disclaimer
    st.markdown("""
    <div class="disclaimer-box">
        ℹ️ <strong>Academic Note:</strong> The <em>Net Recorded Balance</em> is computed directly from recorded transactions and does not represent an actual live bank account balance.
    </div>
    """, unsafe_allow_html=True)

    # Budget Warning Alerts
    warnings = data.get("budget_warnings", [])
    if warnings:
        with st.container():
            st.subheader("⚠️ Monthly Budget Alerts")
            for w in warnings:
                cat = w["category_name"]
                spent = format_inr(w["spent_amount"])
                b_amt = format_inr(w["budget_amount"])
                util = w["utilization_percentage"]
                if w["is_exceeded"]:
                    st.error(f"🚨 **Budget Exceeded:** **{cat}** has spent **{spent}** out of budgeted **{b_amt}** ({util}%).")
                else:
                    st.warning(f"⚠️ **Approaching Limit:** **{cat}** has utilized **{util}%** ({spent} of {b_amt}).")

    st.divider()

    # Visual Charts
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📈 Monthly Income vs. Expenses (6-Month Trend)")
        monthly_trend = data.get("monthly_trend", [])
        if monthly_trend:
            trend_df = pd.DataFrame(monthly_trend)
            chart_df = trend_df.set_index("month_name")[["income", "expense"]]
            chart_df.columns = ["Income", "Expense"]
            st.bar_chart(chart_df, color=["#10B981", "#EF4444"])
        else:
            st.info("No historical monthly data recorded yet.")

    with c2:
        st.subheader(f"🍰 Expense Distribution by Category ({selected_month_name})")
        cat_expenses = data.get("category_expenses", [])
        if cat_expenses:
            cat_df = pd.DataFrame(cat_expenses)
            chart_cat = cat_df.set_index("category")["amount"]
            st.bar_chart(chart_cat, color="#3B82F6")
        else:
            st.info(f"No expense transactions recorded for {selected_month_name} {selected_year}.")

    st.divider()

    # Recent Transactions Table
    st.subheader("🕒 Recent Transactions")
    recent = data.get("recent_transactions", [])
    if recent:
        df_recent = pd.DataFrame(recent)[["date", "type", "category_name", "amount", "payment_method", "description"]]
        df_recent.columns = ["Date", "Type", "Category", "Amount (₹)", "Payment Method", "Description"]
        df_recent["Amount (₹)"] = df_recent["Amount (₹)"].apply(lambda x: f"₹{x:,.2f}")
        st.dataframe(df_recent, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions found. Add a transaction or load demonstration data from the sidebar.")
