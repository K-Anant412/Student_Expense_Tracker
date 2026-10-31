import streamlit as st
from frontend_services.api_client import APIClient


def render_about_view():
    st.title("ℹ️ About the Academic Project")
    st.caption("College submission details, architecture specifications, and demo data utilities.")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("🎓 Academic Project Metadata")
        st.markdown("""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 18px; margin-bottom: 16px;">
            <table style="width: 100%; border-collapse: collapse; font-size: 0.95rem;">
                <tr><td style="padding: 6px; font-weight: 600; color: #475569; width: 40%;">Project Title:</td><td>Student Expense Tracker and Analyzer</td></tr>
                <tr><td style="padding: 6px; font-weight: 600; color: #475569;">Course / Degree:</td><td>Bachelor of Computer Applications (BCA)</td></tr>
                <tr><td style="padding: 6px; font-weight: 600; color: #475569;">College / Institute:</td><td>Shri Shahaji Chhatrapati Mahavidyalaya, Kolhapur</td></tr>
                <tr><td style="padding: 6px; font-weight: 600; color: #475569;">Affiliated University:</td><td>Shivaji University, Kolhapur</td></tr>
                <tr><td style="padding: 6px; font-weight: 600; color: #475569;">Academic Year:</td><td>2026-27</td></tr>
                <tr><td style="padding: 6px; font-weight: 600; color: #475569;">Student Name:</td><td><em>[ Student Name ]</em></td></tr>
                <tr><td style="padding: 6px; font-weight: 600; color: #475569;">Seat Number:</td><td><em>[ Seat Number ]</em></td></tr>
                <tr><td style="padding: 6px; font-weight: 600; color: #475569;">PRN Number:</td><td><em>[ PRN Number ]</em></td></tr>
                <tr><td style="padding: 6px; font-weight: 600; color: #475569;">Project Guide:</td><td><em>[ Asst. Prof. Swati B. Patil ]</em></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🏛️ Architecture & Technology Stack")
        st.markdown("""
        The system implements a decoupled 3-tier architecture:
        - **Frontend Presentation Layer**: Interactive responsive client developed with **Streamlit** on `http://localhost:8501`.
        - **Application / API Tier**: RESTful backend engineered with **Python Flask** on `http://127.0.0.1:5000`.
        - **Persistence Layer**: Relational database storage engineered on **MySQL Server** via **SQLAlchemy / PyMySQL**.
        - **Data Processing & Analytics**: Handled using **Pandas** and Streamlit native visualization components.
        - **Communication Flow**: `Streamlit UI → HTTP JSON Requests → Flask REST API → Service Layer → MySQL Database`.
        """)

    with col2:
        st.subheader("🧪 Demonstration Data Tools")
        st.markdown("""
        For college project demonstration and viva evaluation, you can easily load realistic sample financial records or reset to a clean state.
        """)

        with st.container():
            st.markdown("""
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                <strong>Option A: Seed Demonstration Records</strong>
                <p style="font-size: 0.82rem; color: #64748B; margin-top: 4px;">Loads realistic student income (allowance, freelancing, scholarship), categorized expenses (mess, bus pass, textbooks), and monthly category budgets.</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🌱 Load Academic Demo Data", type="primary", use_container_width=True):
                with st.spinner("Seeding demo records..."):
                    resp = APIClient.seed_demo_data(force=True)
                if resp["ok"]:
                    st.success("✅ Demo records loaded successfully! Check Dashboard and Transactions.")
                    st.rerun()
                else:
                    st.error(f"Failed to seed demo data: {resp['message']}")

        with st.container():
            st.markdown("""
            <div style="background-color: #FEF2F2; border: 1px solid #FECACA; border-radius: 8px; padding: 16px; margin-top: 14px; margin-bottom: 12px;">
                <strong style="color: #991B1B;">Option B: Clear Transactions & Budgets</strong>
                <p style="font-size: 0.82rem; color: #7F1D1D; margin-top: 4px;">Clears all transactions and budgets for starting with an empty database. Preserves standard category classifications.</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🗑️ Reset / Clear All Financial Records", use_container_width=True):
                with st.spinner("Clearing database records..."):
                    resp = APIClient.clear_demo_data()
                if resp["ok"]:
                    st.success("✅ Financial data cleared. Database is now empty and ready for fresh testing.")
                    st.rerun()
                else:
                    st.error(f"Failed to clear data: {resp['message']}")
