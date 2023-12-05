import streamlit as st

def init_section_variables():
    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = ""
