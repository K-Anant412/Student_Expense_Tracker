import streamlit as st
import pandas as pd
from datetime import date, datetime
from frontend_services.api_client import APIClient
from frontend_views.ui_common import format_inr, show_offline_banner


def render_transactions_view():
    st.title("💳 Transaction Management")
    st.caption("View, search, filter, sort, update, and manage your complete transaction history.")

    # Fetch Categories for filter dropdowns
    cat_resp = APIClient.get_categories()
    if not cat_resp["ok"]:
        show_offline_banner()
        return

    all_categories = cat_resp["data"]
    cat_map = {c["id"]: c["name"] for c in all_categories}
    cat_options = ["All"] + [f"{c['name']} ({c['type']})" for c in all_categories]
    cat_id_lookup = {f"{c['name']} ({c['type']})": c["id"] for c in all_categories}

    # Filter Section
    with st.expander("🔍 Filter & Search Records", expanded=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            search_query = st.text_input("Search Keyword", placeholder="Description, category, or payment mode...", key="tx_search")
            type_filter = st.selectbox("Transaction Type", ["All", "Income", "Expense"], key="tx_type_filter")
        with f2:
            selected_cat_str = st.selectbox("Category Filter", cat_options, key="tx_cat_filter")
            selected_cat_id = cat_id_lookup.get(selected_cat_str)
        with f3:
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                start_date = st.date_input("From Date", value=None, key="tx_start_date")
            with d_col2:
                end_date = st.date_input("To Date", value=None, key="tx_end_date")

        s1, s2 = st.columns(2)
        with s1:
            sort_by = st.selectbox("Sort By", ["date", "amount"], format_func=lambda x: "Date" if x == "date" else "Amount", key="tx_sort_by")
        with s2:
            sort_order = st.selectbox("Order", ["desc", "asc"], format_func=lambda x: "Descending (High/Newest to Low/Oldest)" if x == "desc" else "Ascending", key="tx_sort_order")

    # Construct Filter Payload
    filters = {
        "sort_by": sort_by,
        "sort_order": sort_order,
    }
    if search_query.strip():
        filters["search"] = search_query.strip()
    if type_filter != "All":
        filters["type"] = type_filter
    if selected_cat_id:
        filters["category_id"] = selected_cat_id
    if start_date:
        filters["start_date"] = start_date.strftime("%Y-%m-%d")
    if end_date:
        filters["end_date"] = end_date.strftime("%Y-%m-%d")

    # Fetch Transactions
    with st.spinner("Fetching transaction records..."):
        tx_resp = APIClient.get_transactions(filters)

    if not tx_resp["ok"]:
        show_offline_banner()
        return

    transactions = tx_resp["data"]

    # Filtered Summary Metrics
    inc_sum = sum(t["amount"] for t in transactions if t["type"] == "Income")
    exp_sum = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    net_sum = inc_sum - exp_sum

    sm1, sm2, sm3, sm4 = st.columns(4)
    with sm1:
        st.metric("Transactions Found", len(transactions))
    with sm2:
        st.metric("Total Income (Filtered)", format_inr(inc_sum))
    with sm3:
        st.metric("Total Expenses (Filtered)", format_inr(exp_sum))
    with sm4:
        st.metric("Net Surplus / Deficit", format_inr(net_sum))

    st.divider()

    # Display Table
    if transactions:
        df = pd.DataFrame(transactions)
        display_df = df[["id", "date", "type", "category_name", "amount", "payment_method", "description"]].copy()
        display_df.columns = ["ID", "Date", "Type", "Category", "Amount (₹)", "Payment Method", "Description"]
        display_df["Amount (₹)"] = display_df["Amount (₹)"].apply(lambda x: f"₹{x:,.2f}")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions match the selected filter criteria.")

    st.divider()

    # Action Tabs: Edit / Delete
    tab_edit, tab_delete = st.tabs(["✏️ Edit Existing Transaction", "🗑️ Delete Transaction"])

    with tab_edit:
        st.subheader("Edit Transaction Details")
        if not transactions:
            st.info("No transactions available to edit.")
        else:
            tx_options = {f"#{t['id']} | {t['date']} | {t['type']} | {t['category_name']} | ₹{t['amount']}": t for t in transactions}
            selected_tx_label = st.selectbox("Select Transaction to Edit", list(tx_options.keys()), key="edit_select_tx")
            chosen_tx = tx_options[selected_tx_label]

            with st.form("form_edit_transaction"):
                ec1, ec2 = st.columns(2)
                with ec1:
                    edit_type = st.radio("Transaction Type", ["Income", "Expense"], index=0 if chosen_tx["type"] == "Income" else 1, horizontal=True)
                    # Filter categories matching edit_type
                    valid_cats = [c for c in all_categories if c["type"] == edit_type]
                    valid_cat_names = [c["name"] for c in valid_cats]
                    cat_name_to_id = {c["name"]: c["id"] for c in valid_cats}
                    
                    cur_cat_idx = 0
                    if chosen_tx["category_name"] in valid_cat_names:
                        cur_cat_idx = valid_cat_names.index(chosen_tx["category_name"])

                    edit_cat_name = st.selectbox("Category", valid_cat_names, index=cur_cat_idx)
                    edit_amount = st.number_input("Amount (₹)", min_value=1.0, value=float(chosen_tx["amount"]), step=50.0)

                with ec2:
                    current_d = datetime.strptime(chosen_tx["date"], "%Y-%m-%d").date() if chosen_tx["date"] else date.today()
                    edit_date = st.date_input("Transaction Date", value=current_d)
                    
                    pay_methods = ["UPI", "Cash", "Debit Card", "Credit Card", "Net Banking"]
                    cur_pay_idx = pay_methods.index(chosen_tx["payment_method"]) if chosen_tx["payment_method"] in pay_methods else 0
                    edit_pay_method = st.selectbox("Payment Method", pay_methods, index=cur_pay_idx)
                    
                    edit_desc = st.text_input("Description / Note", value=chosen_tx["description"])

                submit_edit = st.form_submit_button("💾 Save Changes", type="primary")

                if submit_edit:
                    cat_id = cat_name_to_id[edit_cat_name]
                    edit_payload = {
                        "type": edit_type,
                        "category_id": cat_id,
                        "amount": edit_amount,
                        "date": edit_date.strftime("%Y-%m-%d"),
                        "payment_method": edit_pay_method,
                        "description": edit_desc.strip(),
                    }
                    u_resp = APIClient.update_transaction(chosen_tx["id"], edit_payload)
                    if u_resp["ok"]:
                        st.success(f"Transaction #{chosen_tx['id']} updated successfully!")
                        st.rerun()
                    else:
                        st.error(f"Failed to update transaction: {u_resp['message']}")

    with tab_delete:
        st.subheader("Delete Transaction Record")
        if not transactions:
            st.info("No transactions available to delete.")
        else:
            del_options = {f"#{t['id']} | {t['date']} | {t['type']} | {t['category_name']} | ₹{t['amount']}": t["id"] for t in transactions}
            selected_del_label = st.selectbox("Select Transaction to Delete", list(del_options.keys()), key="del_select_tx")
            chosen_del_id = del_options[selected_del_label]

            st.warning(f"⚠️ Are you sure you want to permanently delete Transaction **#{chosen_del_id}**? This action cannot be undone.")
            if st.button("🚨 Confirm Delete", type="primary", key="btn_confirm_delete"):
                d_resp = APIClient.delete_transaction(chosen_del_id)
                if d_resp["ok"]:
                    st.success(f"Transaction #{chosen_del_id} deleted successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to delete transaction: {d_resp['message']}")
