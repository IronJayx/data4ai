import streamlit as st

def init_section_variables():
    if 'edited_df' not in st.session_state:
        st.session_state.edited_df = []
    if 'valid_df' not in st.session_state:
        st.session_state.valid_df = []
    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = ''
