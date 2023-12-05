import streamlit as st

from app.services.openai.main import format_for_openai_finetuning

from .config import SUPPORTED_DESTINATIONS
from .strings import EXPORT_MESSAGE, SECTION_TITLE, WARNING_INIT
from .init import init_section_variables


def export_data_section(title_prefix: str = ""):
    init_section_variables()

    if len(st.session_state.valid_df) > 0:
        st.subheader(f"{title_prefix}{SECTION_TITLE}")
        dest_openai, dest_other = st.tabs(SUPPORTED_DESTINATIONS)

        with dest_openai:
            input_list = st.session_state.valid_df.iloc[:,0].tolist()
            output_list = st.session_state.valid_df.iloc[:,1].tolist()
            jsonl_str = format_for_openai_finetuning(st.session_state.system_prompt, input_list, output_list)

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
