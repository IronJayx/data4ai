from io import StringIO
import streamlit as st
import pandas as pd

from .utils import validate_manual_input, process_tabular
from .config import SUPPORTED_INPUT_FORMATS
from .strings import CSV_IMPORT_INFO, CSV_IMPORT_EXAMPLE, FORMAT_NOT_SUPPORTED, SECTION_TITLE, WARNING_INIT
from .init import init_section_variables


def data_import_section(title_prefix: str = ""):

    init_section_variables()

    if len(st.session_state.system_prompt) > 0:
        st.subheader(f"{title_prefix}{SECTION_TITLE}", anchor="step-3")
        st.markdown("Choose import method: ")
        source_csv, source_manual, source_pdf, source_word = st.tabs(
            SUPPORTED_INPUT_FORMATS)

        with source_csv:
            st.info(CSV_IMPORT_INFO)
            with st.expander("See example"):
                st.code(CSV_IMPORT_EXAMPLE)

            uploaded_file = st.file_uploader(
                "Upload a file", key=f"{title_prefix}-base-data", type=[".csv", ".xlsx", ".xls"])

            if uploaded_file is not None:
                st.session_state.input_df = process_tabular(
                    file_path=uploaded_file,
                    name=uploaded_file.name
                )
        with source_manual:
            with st.expander("Provide 10+ examples of ideal input outputs", expanded=False):
                st.session_state.manual_input_list = []
                st.session_state.manual_output_list = []
                # Loop through the current number of rows in the state
                for i in range(st.session_state.num_rows):
                    col1, col2 = st.columns(2)
                    with col1:
                        input_text = st.text_area(
                            f"User Input {i + 1}", key=f"{title_prefix}-{i + 1}-u",)
                    with col2:
                        output_text = st.text_area(
                            f"AI Output {i + 1}", key=f"{title_prefix}-{i + 1}-ai",)

                    if (len(input_text) > 0) & (len(output_text) > 0):
                        st.session_state.manual_input_list.append(input_text)
                        st.session_state.manual_output_list.append(output_text)

                # "+" Button to add one more row
                if st.button('Add More', key=f"{title_prefix}-add"):
                    st.session_state.num_rows += 1  # increase the number of rows by 1

                st.button(label='Validate input', key=f"{title_prefix}-val",
                          use_container_width=True, on_click=validate_manual_input())

        with source_pdf:
            st.markdown(FORMAT_NOT_SUPPORTED)
        with source_word:
            st.markdown(FORMAT_NOT_SUPPORTED)
