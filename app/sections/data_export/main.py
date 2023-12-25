import streamlit as st
import pandas as pd

from app.services.openai.main import format_for_openai_finetuning
from .config import SUPPORTED_DESTINATIONS
from .strings import EXPORT_MESSAGE, SECTION_TITLE, WARNING_INIT
from .init import init_section_variables
from .utils import get_discussion_lists


def export_data_section(title_prefix: str = ""):
    init_section_variables()

    if len(st.session_state.valid_df) > 0:
        st.subheader(f"{title_prefix}{SECTION_TITLE}")
        dest_openai, dest_other = st.tabs(SUPPORTED_DESTINATIONS)

        with dest_openai:
            # Iterate over each row and construct discussions
            messages = get_discussion_lists(df=st.session_state.valid_df)

            jsonl_str = format_for_openai_finetuning(
                system_message=st.session_state.system_prompt, messages=messages
            )

            if jsonl_str:
                jsonl_bytes = str.encode(jsonl_str)
                unique_id = f"l-{len(st.session_state.valid_df)}-h5{str(hash(jsonl_str))[:5]}"
                filename = f'openai-fine-tuning-{unique_id}.jsonl'

                st.markdown(EXPORT_MESSAGE)
                st.markdown(f'Download it as {filename}')
                st.download_button(
                    label="Download",
                    data=jsonl_bytes,
                    file_name=filename,
                    mime="text/jsonl",
                )
