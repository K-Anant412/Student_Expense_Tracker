"""
Streamlit Application Entry Point Wrapper.
Allows launching via `streamlit run app_ui.py` as an alias for `streamlit run streamlit_app.py`.
"""
import runpy

if __name__ == "__main__":
    runpy.run_module("streamlit_app", run_name="__main__")
