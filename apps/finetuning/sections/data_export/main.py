import streamlit as st

from services.openai.main import format_for_openai_finetuning

from .config import SUPPORTED_DESTINATIONS, OPENAI_EXPORTS, OPENAI_EXPORTS_ASSITANT
from .strings import SECTION_TITLE
from .init import init_section_variables
from .utils import get_discussion_lists, download_jsonl
from .finetuning import deploy_fine_tuning
from .assistant import deploy_assistant


def export_data_section(title_prefix: str = ""):
    init_section_variables()

    if len(st.session_state.valid_df) > 0:
        st.subheader(f"{title_prefix}{SECTION_TITLE}")
        dest_openai, dest_other = st.tabs(SUPPORTED_DESTINATIONS)

        with dest_openai:
            # Iterate over each row and construct discussions
            messages = get_discussion_lists(df=st.session_state.valid_df)

            jsonl_str = format_for_openai_finetuning(
                system_message=st.session_state.system_prompt,
                messages=messages
            )

            if jsonl_str:

                download, deploy = st.tabs(OPENAI_EXPORTS)

                with download:
                    download_jsonl(jsonl_str)

                with deploy:
                    deploy_fine_tuning(jsonl_str)


def export_data_assistant(title_prefix: str = ""):
    st.subheader(f"{title_prefix}Deploy your assistant")
    dest_openai, dest_other = st.tabs(SUPPORTED_DESTINATIONS)

    with dest_openai:

        deploy, download = st.tabs(OPENAI_EXPORTS_ASSITANT)

        with download:
            pass
        with deploy:
            deploy_assistant(file_ids=[])
