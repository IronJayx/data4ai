import os
import pandas as pd
import streamlit as st

from .config import DATA_COLUMNS


def validate_manual_input():
    input_list = st.session_state.manual_input_list
    output_list = st.session_state.manual_output_list

    if len(input_list) < 10 or len(output_list) < 10:
        st.warning(
            body='Please input at least 10 examples. That is an OpenAI requirement.', icon="⚠️")
    else:
        # Create a combined list of dictionaries, each with a unique discussion_id
        combined_list = []
        for i, (inp, out) in enumerate(zip(input_list, output_list)):
            combined_list.append(
                {"discussion_id": i + 1, "role": "user", "content": inp})
            combined_list.append(
                {"discussion_id": i + 1, "role": "assistant", "content": out})

        # Creating DataFrame
        df = pd.DataFrame(combined_list)

        # Set the DataFrame in the session state
        st.session_state.input_df = df


def process_tabular(file_path, name):
    # Determine the file extension
    _, file_extension = os.path.splitext(name)

    # Read the file based on its extension
    if file_extension.lower() == '.csv':
        df = pd.read_csv(file_path, header=None)
    elif file_extension.lower() in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path, header=None)
    else:
        raise ValueError("Unsupported file format")

    # Check if the first row matches the expected column names
    if all(isinstance(item, str) and item.lower() in [col.lower() for col in DATA_COLUMNS] for item in df.iloc[0]):
        # If first row is a header, use it as column names
        df.columns = df.iloc[0]
        df = df.drop(0).reset_index(drop=True)
    else:
        # If no header, assign the default column names
        df.columns = DATA_COLUMNS

    return df
