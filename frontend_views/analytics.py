import streamlit as st
import pandas as pd
from datetime import date
from calendar import month_name
from frontend_services.api_client import APIClient
from frontend_views.ui_common import format_inr, show_offline_banner, MONTH_NAMES, YEARS


def render_analytics_view():
    st.title("📈 Advanced Spending Analytics")
    st.caption("Gain deep insights into spending habits, category breakdowns, savings trends, and month-over-month comparisons.")

    today = date.today()

    # Filter by Month & Year or custom Date Range
    filter_mode = st.radio("Analytics Time Window", ["Calendar Month", "Custom Date Range"], horizontal=True)

    month_val = None
    year_val = None
    start_date_str = None
    end_date_str = None

    if filter_mode == "Calendar Month":
        c1, c2 = st.columns(2)
        with c1:
            sel_m_name = st.selectbox("Month", MONTH_NAMES, index=today.month - 1, key="an_m")
            month_val = MONTH_NAMES.index(sel_m_name) + 1
        with c2:
            year_val = st.selectbox("Year", YEARS, index=YEARS.index(today.year) if today.year in YEARS else 2, key="an_y")
    else:
        d1, d2 = st.columns(2)
        with d1:
            s_date = st.date_input("Start Date", value=date(today.year, 1, 1), key="an_start")
            start_date_str = s_date.strftime("%Y-%m-%d")
        with d2:
            e_date = st.date_input("End Date", value=today, key="an_end")
            end_date_str = e_date.strftime("%Y-%m-%d")

    # Fetch Analytics from Flask API
    with st.spinner("Crunching analytics from MySQL ledger..."):
        resp = APIClient.get_analytics(
            month=month_val,
            year=year_val,
            start_date=start_date_str,
            end_date=end_date_str
        )

    if not resp["ok"]:
        show_offline_banner()
        return

    data = resp["data"]
    total_income = data.get("total_income", 0.0)
    total_expenses = data.get("total_expenses", 0.0)
    net_savings = data.get("net_savings", 0.0)
    avg_monthly_exp = data.get("avg_monthly_expense", 0.0)
    prev_comp = data.get("comparison_with_previous", {})
    cat_dist = data.get("category_distribution", [])
    top_cats = data.get("top_categories", [])
    history_trend = data.get("history_trend", [])

    # KPI Summary Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Income (Period)", format_inr(total_income))
    with k2:
        st.metric("Total Expenses (Period)", format_inr(total_expenses))
    with k3:
        st.metric("Net Savings / Surplus", format_inr(net_savings))
    with k4:
        st.metric("Avg. Monthly Expense", format_inr(avg_monthly_exp))

    st.divider()

    # Month-over-Month Comparison
    if filter_mode == "Calendar Month" and prev_comp:
        st.subheader("🔄 Month-over-Month Performance Comparison")
        prev_name = prev_comp.get("previous_month_name", "Previous Month")
        prev_exp = prev_comp.get("previous_expenses", 0.0)
        exp_delta = prev_comp.get("expense_change_amount", 0.0)
        exp_pct = prev_comp.get("expense_change_pct", 0.0)

        cp1, cp2, cp3 = st.columns(3)
        with cp1:
            st.metric(f"Previous Month ({prev_name}) Expenses", format_inr(prev_exp))
        with cp2:
            delta_color = "inverse" if exp_delta > 0 else "normal"
            st.metric("Expense Difference", format_inr(exp_delta), f"{exp_pct}% vs last month", delta_color=delta_color)
        with cp3:
            inc_delta = prev_comp.get("income_change_amount", 0.0)
            st.metric("Income Difference", format_inr(inc_delta))

        if exp_delta > 0:
            st.warning(f"⚠️ Spending increased by **{format_inr(exp_delta)}** ({exp_pct}%) compared to {prev_name}.")
        elif exp_delta < 0:
            st.success(f"🎉 Great job! Spending decreased by **{format_inr(abs(exp_delta))}** ({abs(exp_pct)}%) compared to {prev_name}.")
        else:
            st.info("Spending stayed identical to the previous month.")

        st.divider()

    # Category Breakdown & Top Categories
    col_chart, col_rank = st.columns([5, 4])

    with col_chart:
        st.subheader("🍩 Expense Breakdown by Category")
        if cat_dist:
            df_cat = pd.DataFrame(cat_dist)
            st.bar_chart(df_cat.set_index("category")["amount"], color="#2563EB")
        else:
            st.info("No expense data recorded in this period.")

    with col_rank:
        st.subheader("🥇 Top Spending Categories")
        if top_cats:
            for rank, c in enumerate(top_cats, 1):
                cat_name = c["category"]
                amt = format_inr(c["amount"])
                pct = c["percentage"]
                st.markdown(f"""
                <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; font-weight: 600;">
                        <span>#{rank} {cat_name}</span>
                        <span style="color: #DC2626;">{amt}</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #64748B;">{pct}% of total period spending</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No category rankings available.")

    st.divider()

    # 12-Month Historical Financial Trend
    st.subheader("📅 12-Month Financial Flow & Savings History")
    if history_trend:
        df_hist = pd.DataFrame(history_trend)
        chart_data = df_hist.set_index("period")[["income", "expense", "savings"]]
        chart_data.columns = ["Income (₹)", "Expenses (₹)", "Net Savings (₹)"]
        st.line_chart(chart_data)
        
        with st.expander("View Numerical Trend Table"):
            tbl_df = df_hist[["period", "income", "expense", "savings"]].copy()
            tbl_df.columns = ["Period", "Income (₹)", "Expenses (₹)", "Net Savings (₹)"]
            tbl_df["Income (₹)"] = tbl_df["Income (₹)"].apply(lambda x: f"₹{x:,.2f}")
            tbl_df["Expenses (₹)"] = tbl_df["Expenses (₹)"].apply(lambda x: f"₹{x:,.2f}")
            tbl_df["Net Savings (₹)"] = tbl_df["Net Savings (₹)"].apply(lambda x: f"₹{x:,.2f}")
            st.dataframe(tbl_df, use_container_width=True, hide_index=True)
    else:
        st.info("No historical financial data recorded yet.")
