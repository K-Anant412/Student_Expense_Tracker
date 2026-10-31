import streamlit as st
import pandas as pd
from datetime import date
from io import StringIO
from frontend_services.api_client import APIClient
from frontend_views.ui_common import format_inr, show_offline_banner


def render_reports_view():
    st.title("📄 Financial Statement & CSV Export")
    st.caption("Generate customized financial statements and download transaction ledgers in CSV format for college submission or personal record-keeping.")

    today = date.today()

    # Filter selections
    with st.expander("🛠️ Configure Report Scope & Filters", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            rep_type = st.selectbox("Transaction Filter", ["All", "Income", "Expense"], key="rep_type")
        with c2:
            rep_start = st.date_input("Start Date", value=date(today.year, 1, 1), key="rep_start")
        with c3:
            rep_end = st.date_input("End Date", value=today, key="rep_end")

    filters = {
        "start_date": rep_start.strftime("%Y-%m-%d") if rep_start else None,
        "end_date": rep_end.strftime("%Y-%m-%d") if rep_end else None,
    }
    if rep_type != "All":
        filters["type"] = rep_type

    # Fetch report data
    with st.spinner("Generating financial statement from Flask API..."):
        resp = APIClient.get_report_data(filters)

    if not resp["ok"]:
        show_offline_banner()
        return

    data = resp["data"]
    summary = data.get("summary", {})
    transactions = data.get("transactions", [])

    tot_tx = summary.get("total_transactions", 0)
    tot_inc = summary.get("total_income", 0.0)
    tot_exp = summary.get("total_expenses", 0.0)
    net_bal = summary.get("net_recorded_balance", 0.0)

    # Summary Metrics Card
    st.subheader("📑 Period Statement Summary")
    st.markdown(f"""
    <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 18px 24px; margin-bottom: 20px;">
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;">
            <div>
                <div style="color: #64748B; font-size: 0.8rem; font-weight: 600;">REPORTING PERIOD</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #0F172A;">{rep_start} to {rep_end}</div>
                <div style="color: #94A3B8; font-size: 0.75rem;">Type: {rep_type}</div>
            </div>
            <div>
                <div style="color: #64748B; font-size: 0.8rem; font-weight: 600;">TOTAL INCOME</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #059669;">{format_inr(tot_inc)}</div>
                <div style="color: #94A3B8; font-size: 0.75rem;">Recorded inflows</div>
            </div>
            <div>
                <div style="color: #64748B; font-size: 0.8rem; font-weight: 600;">TOTAL EXPENSES</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #DC2626;">{format_inr(tot_exp)}</div>
                <div style="color: #94A3B8; font-size: 0.75rem;">Recorded outflows</div>
            </div>
            <div>
                <div style="color: #64748B; font-size: 0.8rem; font-weight: 600;">NET RECORDED BALANCE</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: {'#2563EB' if net_bal >= 0 else '#DC2626'};">{format_inr(net_bal)}</div>
                <div style="color: #94A3B8; font-size: 0.75rem;">Surplus / Deficit</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Transactions List & CSV Export
    st.subheader(f"📋 Detailed Transactions ({tot_tx} record{'s' if tot_tx != 1 else ''})")

    if not transactions:
        st.info("No transaction records found matching the specified parameters.")
    else:
        df = pd.DataFrame(transactions)
        export_df = df[["id", "date", "type", "category_name", "amount", "payment_method", "description"]].copy()
        export_df.columns = ["Transaction_ID", "Date", "Type", "Category", "Amount_INR", "Payment_Method", "Description"]

        # Display formatted table on screen
        display_df = export_df.copy()
        display_df["Amount_INR"] = display_df["Amount_INR"].apply(lambda x: f"₹{x:,.2f}")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Generate CSV String
        csv_buffer = StringIO()
        
        # Write statement header comments into CSV
        csv_buffer.write(f"# Student Expense Tracker and Analyzer - Financial Statement\n")
        csv_buffer.write(f"# Period: {rep_start} to {rep_end}\n")
        csv_buffer.write(f"# Total Transactions: {tot_tx}\n")
        csv_buffer.write(f"# Total Income: INR {tot_inc:,.2f}\n")
        csv_buffer.write(f"# Total Expenses: INR {tot_exp:,.2f}\n")
        csv_buffer.write(f"# Net Balance: INR {net_bal:,.2f}\n")
        csv_buffer.write(f"# Generated On: {datetime_now_str()}\n")
        
        export_df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode("utf-8")

        filename = f"student_expense_report_{rep_start}_{rep_end}.csv"

        st.download_button(
            label="📥 Download Official CSV Report",
            data=csv_bytes,
            file_name=filename,
            mime="text/csv",
            type="primary"
        )


def datetime_now_str():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
