import streamlit as st
from datetime import date
from frontend_services.api_client import APIClient
from frontend_views.ui_common import show_offline_banner, format_inr


def render_add_transaction_view():
    st.title("➕ Record New Transaction")
    st.caption("Add an income or expense entry with appropriate category, amount, and payment details.")

    # Fetch Categories
    cat_resp = APIClient.get_categories()
    if not cat_resp["ok"]:
        show_offline_banner()
        return

    all_categories = cat_resp["data"]

    with st.container():
        st.markdown("""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        """, unsafe_allow_html=True)

        col_type, col_amt = st.columns(2)
        with col_type:
            trans_type = st.radio(
                "Transaction Type",
                ["Expense", "Income"],
                index=0,
                horizontal=True,
                help="Choose Expense for money spent, or Income for money received."
            )

        # Filter categories matching chosen type
        type_categories = [c for c in all_categories if c["type"] == trans_type]
        cat_names = [c["name"] for c in type_categories]
        cat_map = {c["name"]: c["id"] for c in type_categories}

        with col_amt:
            amount_val = st.number_input(
                "Amount (₹) *",
                min_value=0.01,
                value=150.00,
                step=10.00,
                format="%.2f",
                help="Enter a positive monetary value strictly greater than zero."
            )

        col_cat, col_date = st.columns(2)
        with col_cat:
            if not cat_names:
                st.warning(f"No categories available for {trans_type}. Please create one in Category Management.")
                selected_cat_name = None
            else:
                selected_cat_name = st.selectbox(
                    f"Select {trans_type} Category *",
                    cat_names,
                    index=0,
                    help="Categorize this transaction to keep your budgets and analytics accurate."
                )

        with col_date:
            trans_date = st.date_input(
                "Transaction Date *",
                value=date.today(),
                max_value=date(2035, 12, 31),
                help="The date when the transaction occurred."
            )

        col_pay, col_desc = st.columns(2)
        with col_pay:
            payment_methods = ["UPI", "Cash", "Debit Card", "Credit Card", "Net Banking"]
            payment_method = st.selectbox(
                "Payment Method *",
                payment_methods,
                index=0,
                help="Select the payment channel used for this transaction."
            )

        with col_desc:
            description = st.text_input(
                "Description / Note (Optional)",
                placeholder="e.g., Semester textbook, Cafeteria lunch, Monthly allowance...",
                help="Brief note for reference."
            )

        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")

        if st.button("🚀 Record Transaction", type="primary", use_container_width=True):
            if not selected_cat_name:
                st.error("Please select a valid category.")
                return

            if amount_val <= 0:
                st.error("Transaction amount must be strictly greater than zero.")
                return

            cat_id = cat_map[selected_cat_name]
            payload = {
                "type": trans_type,
                "category_id": cat_id,
                "amount": amount_val,
                "date": trans_date.strftime("%Y-%m-%d"),
                "payment_method": payment_method,
                "description": description.strip(),
            }

            with st.spinner("Submitting transaction to backend..."):
                resp = APIClient.create_transaction(payload)

            if resp["ok"]:
                st.success(f"🎉 **{trans_type} recorded successfully!** {selected_cat_name}: {format_inr(amount_val)} via {payment_method}")
                st.balloons()
            else:
                st.error(f"Failed to record transaction: {resp['message']}")
