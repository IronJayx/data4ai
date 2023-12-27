# services/openai_service.py
import os
from openai import OpenAI


def connect(api_token):
    """
    Connects to the OpenAI API using the provided token.
    """
    os.environ["OPENAI_API_KEY"] = api_token
    return OpenAI()


def upload_file_to_openai(client, filepath):
    """
    Uploads a file to OpenAI.
    """
    with open(filepath, 'rb') as file:
        response = client.files.create(file=file, purpose='assistants')
    return response.id


def deploy_assistant(client, assistant_name, assistant_instructions, model, uploaded_file_ids):
    """
    Deploys an assistant with the provided parameters.
    """
    try:
        assistant_params = {
            "name": assistant_name,
            "instructions": assistant_instructions,
            "model": model,
            "tools": [{"type": "code_interpreter"}]
        }

        # Include file_ids if provided
        if uploaded_file_ids:
            assistant_params["file_ids"] = uploaded_file_ids

        assistant = client.beta.assistants.create(**assistant_params)
        return True, f"Assistant successfully created. Assistant ID: {assistant.id}"
    except Exception as e:
        return False, f"Error creating assistant: {e}"
