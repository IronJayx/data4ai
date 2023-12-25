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


def process_csv(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path, header=None)

    # Get the number of columns
    num_cols = len(df.columns)

    # Check the number of columns and update headers accordingly
    if num_cols == 2:
        # Assign all rows to the same Discussion ID (1)
        df.insert(0, "Discussion ID", 1)
        df.columns = DATA_COLUMNS
    elif num_cols == 3:
        df.columns = DATA_COLUMNS
    else:
        raise ValueError("Unsupported number of columns in CSV")

    return df
