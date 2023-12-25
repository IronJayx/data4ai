import streamlit as st
import pandas as pd

from app.services.openai.main import format_for_openai_finetuning
from .config import SUPPORTED_DESTINATIONS, OPENAI_EXPORTS
from .strings import SECTION_TITLE
from .init import init_section_variables
from .utils import get_discussion_lists
from .finetuning import download_finetuned, deploy_fine_tuning


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

                download, deploy = st.tabs(OPENAI_EXPORTS)

                with download:
                    download_finetuned(jsonl_str)

                with deploy:
                    deploy_fine_tuning(jsonl_str)
