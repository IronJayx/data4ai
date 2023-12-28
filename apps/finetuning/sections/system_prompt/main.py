import streamlit as st

from .init import init_section_variables
from .utils import validate_system_prompt
from .strings import SYSTEM_PROMPT_INFO, SYSTEM_PROMPT_EXAMPLE, SECTION_TITLE

def system_prompt_section(title_prefix: str = ""):
    st.subheader(f"{title_prefix}{SECTION_TITLE}", anchor="step-1")

    # description
    st.info(SYSTEM_PROMPT_INFO)

    # init variables
    init_section_variables()

    with st.expander("See example"):
        st.code(SYSTEM_PROMPT_EXAMPLE)

    # input
    st.text_area(
        label="",
        key="system_prompt",
        height=300,
        placeholder="Enter your system prompt here.")
    st.button(label='Done', disabled=len(st.session_state.system_prompt) > 0, use_container_width=True, on_click=validate_system_prompt)
