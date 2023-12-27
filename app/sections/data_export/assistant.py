import streamlit as st
from .utils import connect, upload_file


def deploy_assistant(file_ids: list):
    # User inputs for assistant configuration
    # Input for custom model name or selection from a predefined list
    default_models = ["gpt-3.5-turbo", "babbage-002",
                      "davinci-002", "gpt-4-1106-preview"]
    model = st.selectbox("Base model", default_models)

    with st.expander("Advanced: use a private fine-tuned model"):
        model = st.text_input("Enter a custom fine-tuned model name",
                              placeholder="e.g., ft:gpt-3.5-turbo-0613:personal::8a6Pa3Nl")

    # Input for the assistant's name and instructions
    assistant_name = st.text_input(
        "Enter Assistant Name", placeholder="e.g., Math Tutor")
    assistant_instructions = st.text_area("Enter Instructions for the Assistant",
                                          placeholder="e.g., You are a personal math tutor. Write and run code to answer math questions.")

    client = connect()

    if client:
        # Create an assistant
        if st.button("Deploy Assistant"):
            try:
                assistant_params = {
                    "name": assistant_name,
                    "instructions": assistant_instructions,
                    "model": model,
                    "tools": [{"type": "code_interpreter"}]
                }

                # Include file_ids if provided
                if file_ids:
                    assistant_params["file_ids"] = file_ids

                assistant = client.beta.assistants.create(**assistant_params)
                st.success(f"Assistant created. Assistant ID: {assistant.id}")
            except Exception as e:
                st.error(f"Error creating assistant: {e}")
    else:
        st.warning(
            "Please enter your OpenAI API Token and ensure you have a dataset.")
