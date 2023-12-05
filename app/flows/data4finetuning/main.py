# main.py
import streamlit as st

from app.sections.system_prompt.main import system_prompt_section
from app.sections.data_import.main import data_import_section
from app.sections.validate_data.main import validate_data_section
from app.sections.data_export.main import export_data_section
from .init import init_flow_variables

def data4finetuning():
    st.header("Create a fine-tuning dataset for OpenAI.")

    # init
    init_flow_variables()

    # Execute steps
    system_prompt_section(title_prefix="Step 1: ")

    data_import_section(title_prefix="Step 2: ")

    validate_data_section(title_prefix="Step 3: ")

    export_data_section(title_prefix="Step 4: ")
