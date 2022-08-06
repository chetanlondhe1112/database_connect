# Database:testdb, Table: trial_sheet, Table_names= "Underscored"
import streamlit as st

def dashboard(status):
    if status:
        return st.markdown(f'# Welcome *{st.session_state["username"]}*'), st.markdown("""---""")
    else:
        return st.warning("Please login first.")

dashboard(st.session_state["authentication_status"])