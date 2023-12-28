import streamlit as st

from .utils import connect, upload_file


def deploy_fine_tuning(jsonl_str):
    st.subheader("Deploy Fine-Tuning Job")

    client = connect()

    if client:
        advanced = False

        training_file_id = upload_file(
            client=client, content=jsonl_str, purpose='fine-tune')

        # User inputs for fine-tuning job configuration
        model = st.selectbox(
            "Select Model", ["gpt-3.5-turbo", "babbage-002", "davinci-002"])

        with st.expander("Parameters (advanced)"):
            n_epochs = st.number_input(
                "Number of Epochs", min_value=1, value=3)
            learning_rate_multiplier = st.number_input(
                "Learning Rate Multiplier", value=1.0)
            batch_size = st.number_input("Batch Size", min_value=1, value=4)
            advanced = True

        # Launch button
        if st.button("Start Fine-Tuning Job"):
            try:
                if advanced:
                    job = client.fine_tuning.jobs.create(
                        training_file=training_file_id,
                        model=model,
                        hyperparameters={
                            "n_epochs": n_epochs,
                            "learning_rate_multiplier": learning_rate_multiplier,
                            "batch_size": batch_size
                        }
                    )
                else:
                    job = client.fine_tuning.jobs.create(
                        training_file=training_file_id,
                        model=model,
                    )
                st.success(f"Fine-tuning job started. Job ID: {job.id}")
            except Exception as e:
                st.error(f"Error starting fine-tuning job: {e}")
    else:
        st.warning(
            "Please enter your OpenAI API Token and ensure you have a dataset.")
