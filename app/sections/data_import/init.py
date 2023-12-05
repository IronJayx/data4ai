import streamlit as st

def init_section_variables():
    if 'input_df' not in st.session_state:
        st.session_state.input_df = []
