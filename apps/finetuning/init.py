import streamlit as st

from config import OPENAI_MIN_FINETUNING_EXAMPLES


def init_flow_variables():
    if 'num_rows' not in st.session_state:
        st.session_state.num_rows = OPENAI_MIN_FINETUNING_EXAMPLES
