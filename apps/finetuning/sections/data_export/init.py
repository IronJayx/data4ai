import streamlit as st

def init_section_variables():
    if 'valid_df' not in st.session_state:
        st.session_state.valid_df = []
