import pandas as pd
import streamlit as st

from .config import DATA_COLUMNS

def validate_manual_input():
    input = st.session_state.manual_input_list
    output = st.session_state.manual_output_list

    if (len(input) < 10) | (len(output) < 10):
        st.warning(body='Please input at least 10 examples. That is an OpenAI requirement.', icon="⚠️")
    else:
        st.write(input)
        st.session_state.input_df = pd.DataFrame(data={
            DATA_COLUMNS[0]: input,
            DATA_COLUMNS[1]: output
        })
