import streamlit as st

def validate_system_prompt():
    if len(st.session_state.system_prompt) == 0:
        st.warning(body='Please input your system prompt, the system prompt cannot be empty.', icon="⚠️")
