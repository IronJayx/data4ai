import streamlit as st


def validate_edited_df():
    df = st.session_state.edited_df
    st.session_state.valid_df = df
