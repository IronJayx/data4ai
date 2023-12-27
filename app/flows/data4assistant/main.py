# main.py
import os
import tempfile
import streamlit as st

from openai import OpenAI


from app.services.scraper.main import crawl, analyze_url_texts, split_into_files


def deploy_assistant(client):
    # User inputs for assistant configuration
    # Input for custom model name or selection from a predefined list
    default_models = ["gpt-3.5-turbo-1106"]
    model = st.selectbox("Base model", default_models)

    # Input for the assistant's name and instructions
    assistant_name = st.text_input(
        "Enter Assistant Name", placeholder="e.g., Streamlit Assistant")
    assistant_instructions = st.text_area("Enter Instructions for the Assistant",
                                          placeholder="e.g., You are a coding assistant enriched with Streamlit documentation. You will answer request to help build and debug Streamlit applications")

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
                if 'uploaded_file_ids' in st.session_state:
                    assistant_params["file_ids"] = st.session_state['uploaded_file_ids']

                assistant = client.beta.assistants.create(**assistant_params)
                st.success(
                    f"Assistant sucessfully created. Assistant ID: {assistant.id}")
                st.success(
                    "You can access it at: https://platform.openai.com/assistants")
            except Exception as e:
                st.error(f"Error creating assistant: {e}")
    else:
        st.warning(
            "Please enter your OpenAI API Token and ensure you have a dataset.")


def connect():
    # User inputs OpenAI API token
    api_token = st.text_input("Enter your OpenAI API Token", type="password")

    if api_token:
        # Export the API token as an environment variable
        os.environ["OPENAI_API_KEY"] = api_token

        client = OpenAI()

        return client


def upload_file_to_openai(client, filepath):
    with open(filepath, 'rb') as file:
        response = client.files.create(file=file, purpose='assistants')
    return response.id


def main():
    st.title("Web2GPT Assistant")
    st.markdown("""
        #### Create a custom GPT-assistant augmented with domain-specific knowledge from a web domain.\n
    """)
    with st.expander("More on how it works"):
        st.text("""

                You will need to provide two things:

                - an URL: the app will scrap this URL and all "childs" urls it finds starting with the same domain name.
                - you OpenAI key: this will be used to upload scraped information to your OpenAI account and deploy  a customized assistant.

                Once launched the app will:

                - Scrap the website and its child urls
                - Split scraped information across <= 20 files (openai api only supports 20 files per assistant)
                - Deploy your assistant

                 Note: we don't store your OpenAI key.
        """)

    st.subheader(f"Step 1: Enter an url to retrieve information")

    # data retrieval section

    # URL input

    base_url = st.text_input("Enter the URL to scrap:", "")

    # OpenAI key input
    client = connect()

    # Scraping button

    if st.button("Start Scraping"):
        if base_url:
            visited_urls = set()
            url_texts = {}

            # Create a placeholder for the current URL
            current_url_placeholder = st.empty()

            with st.spinner("Scraping urls..."):
                for current_url in crawl(base_url, base_url, visited_urls, url_texts):
                    # Update the placeholder with the current URL
                    current_url_placeholder.warning(current_url)

            num_urls, total_text_size_mb = analyze_url_texts(url_texts)
            st.success(
                f"Scraping completed. {num_urls} URLs scraped. Total text size: {total_text_size_mb:.4f} MB")

            # Clear the current URL placeholder after completion
            current_url_placeholder.empty()

        # Store the results in Streamlit's session state
        st.session_state['url_texts'] = url_texts

    # Create a temporary directory

    temp_dir = tempfile.mkdtemp()

    # Split files button

    if 'url_texts' in st.session_state:
        created_files = split_into_files(
            st.session_state['url_texts'], temp_dir, base_url)
        st.session_state['created_files'] = created_files
        st.success(
            f"Scraping finished.\n Results splitted across: {len(created_files)} files")
    else:
        st.warning("Enter an url of a website to scrape.")

    # Step 3: Upload Section

    st.subheader(f"Step 2: Upload files to OpenAI for retrieval")

    if 'created_files' in st.session_state:
        if client:
            if st.button("Upload Files"):
                if client and 'created_files' in st.session_state:
                    uploaded_file_ids = []
                    with st.spinner("Uploading files..."):
                        for file_path in st.session_state['created_files']:
                            file_id = upload_file_to_openai(client, file_path)
                            uploaded_file_ids.append(file_id)

                    st.session_state['uploaded_file_ids'] = uploaded_file_ids
                    st.success("Files uploaded successfully.")
                elif not client:
                    st.error("Please enter a valid OpenAI API token.")
                else:
                    st.error(
                        "No files available to upload. Please create files first.")

    st.subheader(f"Step 3: Deploy your assistant")

    if client and 'uploaded_file_ids' in st.session_state:
        deploy_assistant(client)
