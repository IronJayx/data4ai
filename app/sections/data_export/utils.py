import os
import tempfile
import streamlit as st
from openai import OpenAI

from .strings import EXPORT_MESSAGE


def validate_edited_df():
    df = st.session_state.edited_df
    st.session_state.valid_df = df


def get_discussion_lists(df):
    # Group by Discussion ID and iterate through each group
    grouped = df.groupby('discussion_id')
    discussion_lists = {}

    for discussion_id, group in grouped:
        # Create a list of message dictionaries for each discussion
        messages = group.apply(
            lambda row: {"role": row['role'], "content": row['content']}, axis=1).tolist()
        discussion_lists[discussion_id] = messages

    return discussion_lists


def upload_file(client, content, purpose):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.jsonl') as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    # Upload the file using its path
    file_response = client.files.create(
        file=open(temp_file_path, 'rb'),
        purpose=purpose
    )
    training_file_id = file_response.id

    return training_file_id


def connect():
    # User inputs OpenAI API token
    api_token = st.text_input("Enter your OpenAI API Token", type="password")

    if api_token:
        # Export the API token as an environment variable
        os.environ["OPENAI_API_KEY"] = api_token

        client = OpenAI()

        return client


def download_jsonl(jsonl_str):
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
