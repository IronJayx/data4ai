import streamlit as st

from .utils import validate_edited_df
from .strings import SECTION_TITLE, WARNING_INIT
from .init import init_section_variables

def validate_data_section(title_prefix: str = ""):
    init_section_variables()

    if (len(st.session_state.input_df) > 0) & (len(st.session_state.system_prompt) > 0):
        st.subheader(f"{title_prefix}{SECTION_TITLE}", anchor="step-3")
        st.session_state.edited_df = st.data_editor(
            st.session_state.input_df,
            num_rows="dynamic",
            use_container_width=True
        )
        st.button(label='Export', use_container_width=True, on_click=validate_edited_df)
