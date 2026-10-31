import streamlit as st
import pandas as pd
from frontend_services.api_client import APIClient
from frontend_views.ui_common import show_offline_banner


def render_categories_view():
    st.title("🏷️ Category System Management")
    st.caption("Organize your income streams and expense categories. Consistent categories ensure reliable budget alerts and analytics.")

    # Fetch all categories
    with st.spinner("Loading categories..."):
        resp = APIClient.get_categories()

    if not resp["ok"]:
        show_offline_banner()
        return

    all_cats = resp["data"]
    exp_cats = [c for c in all_cats if c["type"] == "Expense"]
    inc_cats = [c for c in all_cats if c["type"] == "Income"]

    col_exp, col_inc = st.columns(2)

    with col_exp:
        st.subheader(f"🔴 Expense Categories ({len(exp_cats)})")
        if exp_cats:
            df_exp = pd.DataFrame(exp_cats)[["id", "name", "description", "is_default"]]
            df_exp.columns = ["ID", "Category Name", "Description", "Standard Default"]
            st.dataframe(df_exp, use_container_width=True, hide_index=True)
        else:
            st.info("No expense categories found.")

    with col_inc:
        st.subheader(f"🟢 Income Categories ({len(inc_cats)})")
        if inc_cats:
            df_inc = pd.DataFrame(inc_cats)[["id", "name", "description", "is_default"]]
            df_inc.columns = ["ID", "Category Name", "Description", "Standard Default"]
            st.dataframe(df_inc, use_container_width=True, hide_index=True)
        else:
            st.info("No income categories found.")

    st.divider()

    # Create & Delete Tabs
    t_add, t_del = st.tabs(["➕ Create Custom Category", "🗑️ Delete Category"])

    with t_add:
        st.subheader("Add a New Financial Category")
        with st.form("form_create_category"):
            ac1, ac2 = st.columns(2)
            with ac1:
                new_cat_name = st.text_input("Category Name *", placeholder="e.g., Gym & Fitness, Club Subscriptions...")
                new_cat_type = st.selectbox("Category Type *", ["Expense", "Income"])
            with ac2:
                new_cat_desc = st.text_input("Description / Purpose", placeholder="Optional description...")

            submit_cat = st.form_submit_button("💾 Save Category", type="primary")

            if submit_cat:
                if not new_cat_name.strip():
                    st.error("Category name cannot be empty.")
                else:
                    payload = {
                        "name": new_cat_name.strip(),
                        "type": new_cat_type,
                        "description": new_cat_desc.strip(),
                    }
                    c_resp = APIClient.create_category(payload)
                    if c_resp["ok"]:
                        st.success(f"Category '{new_cat_name.strip()}' created successfully!")
                        st.rerun()
                    else:
                        st.error(f"Failed to create category: {c_resp['message']}")

    with t_del:
        st.subheader("Safely Remove an Unused Category")
        st.info("ℹ️ Categories that are currently associated with recorded transactions or active monthly budgets cannot be deleted to preserve financial ledger integrity.")

        # Exclude default categories if needed or allow deletion if not in use
        cat_choices = {f"#{c['id']} | {c['name']} ({c['type']})": c["id"] for c in all_cats}
        if not cat_choices:
            st.info("No categories available.")
        else:
            selected_choice = st.selectbox("Select Category to Delete", list(cat_choices.keys()), key="del_cat_choice")
            selected_cat_id = cat_choices[selected_choice]

            if st.button("🚨 Delete Selected Category", type="primary", key="btn_del_cat"):
                d_resp = APIClient.delete_category(selected_cat_id)
                if d_resp["ok"]:
                    st.success("Category deleted successfully!")
                    st.rerun()
                else:
                    st.error(f"Cannot delete category: {d_resp['message']}")
