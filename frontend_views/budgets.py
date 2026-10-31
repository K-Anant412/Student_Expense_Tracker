import streamlit as st
import pandas as pd
from datetime import date
from calendar import month_name
from frontend_services.api_client import APIClient
from frontend_views.ui_common import format_inr, show_offline_banner, MONTH_NAMES, YEARS


def render_budgets_view():
    st.title("🎯 Monthly Category Budgets")
    st.caption("Plan and monitor monthly spending limits for individual expense categories to avoid overspending.")

    today = date.today()

    # Filter Bar
    b1, b2, b3 = st.columns([2, 2, 4])
    with b1:
        sel_month_name = st.selectbox("Budget Month", MONTH_NAMES, index=today.month - 1, key="budget_month")
        sel_month = MONTH_NAMES.index(sel_month_name) + 1
    with b2:
        sel_year = st.selectbox("Budget Year", YEARS, index=YEARS.index(today.year) if today.year in YEARS else 2, key="budget_year")
    with b3:
        threshold = st.slider("Warning Alert Threshold (%)", min_value=50, max_value=95, value=80, step=5, help="Categories utilizing more than this threshold trigger an alert.")

    # Fetch Category Budget Status
    with st.spinner("Calculating budget allocations and actual expenses..."):
        resp = APIClient.get_budget_status(month=sel_month, year=sel_year, threshold=threshold)

    if not resp["ok"]:
        show_offline_banner()
        return

    data = resp["data"]
    total_budget = data.get("total_budget", 0.0)
    total_spent = data.get("total_spent_in_budgeted_categories", 0.0)
    remaining_total = data.get("overall_remaining", 0.0)
    overall_util = data.get("overall_utilization", 0.0)
    budget_items = data.get("items", [])

    # Overview Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Monthly Budget", format_inr(total_budget))
    with m2:
        st.metric("Total Spent (Budgeted)", format_inr(total_spent))
    with m3:
        st.metric("Remaining Budget", format_inr(remaining_total))
    with m4:
        st.metric("Overall Utilization", f"{overall_util}%")

    # Progress bar for overall budget
    st.write(f"**Overall Budget Usage for {sel_month_name} {sel_year}:**")
    progress_val = min(float(overall_util) / 100.0, 1.0)
    st.progress(progress_val)

    st.divider()

    # Display Category Budgets
    st.subheader(f"📋 Category Budgets for {sel_month_name} {sel_year}")

    if not budget_items:
        st.info(f"No budgets configured for {sel_month_name} {sel_year}. Use the form below to set spending targets for your expense categories.")
    else:
        for item in budget_items:
            cat_name = item["category_name"]
            b_amt = item["budget_amount"]
            spent = item["spent_amount"]
            rem = item["remaining_amount"]
            util = item["utilization_percentage"]
            status = item["status"]

            # Visual color scheme based on status
            if status == "Exceeded":
                card_border = "#EF4444"
                badge_class = "badge-danger"
                status_label = f"🚨 Exceeded by {format_inr(spent - b_amt)}"
            elif status == "Warning":
                card_border = "#F59E0B"
                badge_class = "badge-warning"
                status_label = f"⚠️ Warning ({util}%)"
            else:
                card_border = "#10B981"
                badge_class = "badge-normal"
                status_label = "✅ Within Limit"

            st.markdown(f"""
            <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-left: 5px solid {card_border}; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 1.1rem; font-weight: 700; color: #0F172A;">{cat_name}</span>
                    <span class="{badge_class}">{status_label}</span>
                </div>
                <div style="margin-top: 8px; font-size: 0.9rem; color: #475569; display: flex; justify-content: space-between;">
                    <span>Budget: <strong>{format_inr(b_amt)}</strong></span>
                    <span>Spent: <strong>{format_inr(spent)}</strong></span>
                    <span>Remaining: <strong>{format_inr(rem)}</strong></span>
                    <span>Utilization: <strong>{util}%</strong></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(min(float(util) / 100.0, 1.0))

    st.divider()

    # Form to Set or Update Category Budget
    t1, t2 = st.tabs(["➕ Set / Update Category Budget", "🗑️ Delete Category Budget"])

    # Fetch Expense Categories
    cat_resp = APIClient.get_categories(cat_type="Expense")
    expense_cats = cat_resp["data"] if cat_resp["ok"] else []
    exp_cat_names = [c["name"] for c in expense_cats]
    exp_cat_map = {c["name"]: c["id"] for c in expense_cats}

    with t1:
        st.subheader("Add or Modify a Monthly Category Budget")
        with st.form("form_create_budget"):
            c_cat, c_amt = st.columns(2)
            with c_cat:
                if not exp_cat_names:
                    st.warning("No expense categories found.")
                    chosen_exp_cat = None
                else:
                    chosen_exp_cat = st.selectbox("Expense Category", exp_cat_names, key="budget_set_cat")
            with c_amt:
                budget_amount_val = st.number_input("Monthly Budget Limit (₹)", min_value=100.0, value=2000.0, step=100.0)

            c_m, c_y = st.columns(2)
            with c_m:
                set_month_name = st.selectbox("Month", MONTH_NAMES, index=sel_month - 1, key="budget_set_month")
                set_month = MONTH_NAMES.index(set_month_name) + 1
            with c_y:
                set_year = st.selectbox("Year", YEARS, index=YEARS.index(sel_year) if sel_year in YEARS else 2, key="budget_set_year")

            submit_b = st.form_submit_button("💾 Save Budget Target", type="primary")

            if submit_b:
                if not chosen_exp_cat:
                    st.error("Please choose a valid expense category.")
                else:
                    cat_id = exp_cat_map[chosen_exp_cat]
                    # Check if budget already exists for this cat, month, year
                    existing_b = next((it for it in budget_items if it["category_id"] == cat_id and it["month"] == set_month and it["year"] == set_year), None)
                    
                    if existing_b:
                        # Update
                        u_resp = APIClient.update_budget(existing_b["budget_id"], {"amount": budget_amount_val})
                        if u_resp["ok"]:
                            st.success(f"Updated budget for {chosen_exp_cat} in {set_month_name} {set_year} to {format_inr(budget_amount_val)}!")
                            st.rerun()
                        else:
                            st.error(f"Failed to update budget: {u_resp['message']}")
                    else:
                        # Create
                        payload = {
                            "category_id": cat_id,
                            "month": set_month,
                            "year": set_year,
                            "amount": budget_amount_val,
                        }
                        c_resp = APIClient.create_budget(payload)
                        if c_resp["ok"]:
                            st.success(f"Budget for {chosen_exp_cat} in {set_month_name} {set_year} set to {format_inr(budget_amount_val)}!")
                            st.rerun()
                        else:
                            st.error(f"Failed to create budget: {c_resp['message']}")

    with t2:
        st.subheader("Remove a Category Budget")
        if not budget_items:
            st.info("No active budgets in this period to delete.")
        else:
            del_b_options = {f"#{it['budget_id']} | {it['category_name']} | Budget: {format_inr(it['budget_amount'])}": it["budget_id"] for it in budget_items}
            chosen_del_label = st.selectbox("Select Budget to Remove", list(del_b_options.keys()), key="select_del_budget")
            chosen_b_id = del_b_options[chosen_del_label]

            if st.button("🚨 Delete Budget", type="primary", key="btn_del_budget"):
                d_resp = APIClient.delete_budget(chosen_b_id)
                if d_resp["ok"]:
                    st.success("Budget record deleted successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to delete budget: {d_resp['message']}")
