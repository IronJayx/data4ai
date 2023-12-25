import os
import tempfile
import streamlit as st
from openai import OpenAI

from .strings import EXPORT_MESSAGE


def upload_file(client, content):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.jsonl') as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    # Upload the file using its path
    file_response = client.files.create(
        file=open(temp_file_path, 'rb'),
        purpose="fine-tune"
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


def deploy_fine_tuning(jsonl_str):
    st.subheader("Deploy Fine-Tuning Job")

    client = connect()

    st.write(client)

    if client:

        training_file_id = upload_file(client=client, content=jsonl_str)

        # User inputs for fine-tuning job configuration
        model = st.selectbox(
            "Select Model", ["gpt-3.5-turbo", "babbage-002", "davinci-002"])
        n_epochs = st.number_input("Number of Epochs", min_value=1, value=3)
        learning_rate_multiplier = st.number_input(
            "Learning Rate Multiplier", value=1.0)
        batch_size = st.number_input("Batch Size", min_value=1, value=4)

        # Launch button
        if st.button("Start Fine-Tuning Job"):
            try:
                job = client.fine_tuning.jobs.create(
                    training_file=training_file_id,
                    model=model,
                    hyperparameters={
                        "n_epochs": n_epochs,
                        "learning_rate_multiplier": learning_rate_multiplier,
                        "batch_size": batch_size
                    }
                )
                st.success(f"Fine-tuning job started. Job ID: {job.id}")
                st.write(job)
            except Exception as e:
                st.error(f"Error starting fine-tuning job: {e}")
    else:
        st.warning(
            "Please enter your OpenAI API Token and ensure you have a dataset.")


def download_finetuned(jsonl_str):
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
