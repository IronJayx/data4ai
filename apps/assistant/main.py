# main.py
import os
import tempfile
import streamlit as st
from services.scraper import crawl, sanitize_url_for_filename
from services.data_processing import analyze_dict, split_into_files
from services.openai import connect, upload_file_to_openai, deploy_assistant


def data_retrieval_section():
    base_url = st.text_input("Enter the URL to scrap:", "")
    if st.button("Start Scraping") and base_url:
        visited_urls = set()
        url_texts = {}
        current_url_placeholder = st.empty()
        with st.spinner("Scraping urls..."):
            for current_url in crawl(base_url, base_url, visited_urls, url_texts):
                current_url_placeholder.warning(current_url)
        num_urls, total_text_size_mb = analyze_dict(url_texts)
        st.success(
            f"Scraping completed. {num_urls} URLs scraped. Total text size: {total_text_size_mb:.4f} MB")
        current_url_placeholder.empty()
        st.session_state['url_texts'] = url_texts
    return base_url


def file_creation_and_splitting_section(base_url):
    temp_dir = tempfile.mkdtemp()
    if 'url_texts' in st.session_state:
        created_files = split_into_files(
            st.session_state['url_texts'], temp_dir, sanitize_url_for_filename(base_url))
        st.session_state['created_files'] = created_files
        st.success(
            f"Scraping finished.\n Results splitted across: {len(created_files)} files")


def file_upload_section(client):
    if 'created_files' in st.session_state and client:
        if st.button("Upload Files"):
            uploaded_file_ids = []
            with st.spinner("Uploading files..."):
                for file_path in st.session_state['created_files']:
                    file_id = upload_file_to_openai(client, file_path)
                    uploaded_file_ids.append(file_id)
            st.session_state['uploaded_file_ids'] = uploaded_file_ids
            st.success("Files uploaded successfully.")


def download_files_section():
    if 'created_files' in st.session_state:
        st.write("Download the scraped data files:")
        for file_path in st.session_state['created_files']:
            with open(file_path, "rb") as file:
                btn = st.download_button(
                    label="Download " + os.path.basename(file_path),
                    data=file,
                    file_name=os.path.basename(file_path),
                    mime="text/plain"
                )


def assistant_deployment_section(client):
    if client and 'uploaded_file_ids' in st.session_state:
        assistant_name = st.text_input(
            "Enter Assistant Name", placeholder="e.g., Streamlit Assistant")
        assistant_instructions = st.text_area("Enter Instructions for the Assistant",
                                              placeholder="e.g., You are a coding assistant enriched with Streamlit documentation. You will answer request to help build and debug Streamlit applications")
        default_models = ["gpt-3.5-turbo-1106"]
        model = st.selectbox("Base model", default_models)
        if st.button("Deploy Assistant"):
            success, message = deploy_assistant(
                client, assistant_name, assistant_instructions, model, st.session_state['uploaded_file_ids'])
            if success:
                st.success(message)
            else:
                st.error(message)


def main():
    st.title("Web2GPT Assistant")
    # ... [description and expander code]

    base_url = data_retrieval_section()

    # Only show Step 2 if URLs have been successfully scraped
    if 'url_texts' in st.session_state:
        st.subheader("Step 2: Create and split files")
        file_creation_and_splitting_section(base_url)

        # Only show Step 3 if files have been created and split
        if 'created_files' in st.session_state:
            st.subheader(
                "Step 3: Download or Upload files to OpenAI for retrieval")

            tab1, tab2 = st.tabs(
                ["Upload Files to OpenAI", "Download Files Locally"])

            with tab1:
                api_token = st.text_input(
                    "Enter your OpenAI API Token", type="password")
                client = connect(api_token) if api_token else None
                file_upload_section(client)

                # Only show Step 4 if either files have been uploaded or API token is entered
                if 'uploaded_file_ids' in st.session_state or client:
                    st.subheader("Step 4: Deploy your assistant")
                    assistant_deployment_section(client)

            with tab2:
                download_files_section()


if __name__ == "__main__":
    main()
