import streamlit as st
from app.openai.main import format_for_openai_finetuning
import pandas as pd
from io import StringIO

OPEN_AI_MIN_FINETUNING_EXAMPLES = 10
DATA_COLUMNS = ["User Query", "Model Answer"]
SUPPORTED_INPUT_FORMATS = ["CSV", "Manual", "Excel (soon)", "Pdf (soon)", "Word (soon)"]

if 'num_rows' not in st.session_state:
    st.session_state.num_rows = OPEN_AI_MIN_FINETUNING_EXAMPLES
if 'input_df' not in st.session_state:
    st.session_state.input_df = []
if 'edited_df' not in st.session_state:
    st.session_state.edited_df = []
if 'valid_df' not in st.session_state:
    st.session_state.valid_df = []

st.header(
    "Create a fine-tuning your LLM chat model."
)

# functions

def validate_edited_df():
    df = st.session_state.edited_df

    st.session_state.valid_df = df

def validate_system_prompt():
    if len(st.session_state.system_prompt) == 0:
        st.warning(body='Please input your system prompt, the system prompt cannot be empty.', icon="⚠️")

def validate_manual_input():
    input = st.session_state.manual_input_list
    output = st.session_state.manual_output_list

    if (len(input) < 10) | (len(output) < 10):
        st.warning(body='Please input at least 10 examples. That is an OpenAI requirement.', icon="⚠️")
    else:
        st.write(input)
        st.session_state.input_df = pd.input_df(data={
            DATA_COLUMNS[0]: input,
            DATA_COLUMNS[1]: output
        })

# Step 1

st.subheader("Step 1: Enter the system prompt")
st.info("""
    The system prompt contains instructions on how the model should behave.
    """)
with st.expander("See example"):
    st.code("""
        You are a geography expert capable.
        Users will ask you question on wether a city is the capital of a country.

        You should provide concise responses like so:
        - If the city is the capital of the mentioned country answer Yes.
        - If the city is belongs to the mentioned country but is not a capital answer No.
        - If the country mentioned is not a country tell the user so.
        - If the city mentioned is not a city tell the user so.
    """)
st.text_area(
    label="",
    key="system_prompt",
    height= 300,
    placeholder="Enter your system prompt here.")
st.button(label='Done', disabled=len(st.session_state.system_prompt) > 0, use_container_width=True, on_click=validate_system_prompt)

# Step 2

if len(st.session_state.system_prompt) > 0:
    st.subheader("Step 2: Import your data", anchor="step-2")
    st.markdown("Choose import method: ")
    source_csv, source_manual, source_excel, source_pdf, source_word = st.tabs(SUPPORTED_INPUT_FORMATS)

    with source_csv:
        st.info("""
            Format: Your csv must have two columns with NO headers and at least 10 examples.

            - The first column should contains the user request to the model.
            - The second column should contains the model response to that request.
            """)
        with st.expander("See example"):
            st.code("""
                What is the capital of France ?, Paris
                What is the capital of Germany ?, Berlin
                What is the capital of America ?, America is not a country
                What is the capital of the US ?, Washington
                What is the capital of France ?, Paris
                What is the capital of Germany ?, Berlin
                What is the capital of America ?, America is not a country
                What is the capital of the US ?, Washington
                What is the capital of France ?, Paris
                What is the capital of Germany ?, Berlin
            """)

        uploaded_file = st.file_uploader("Upload a file", type=[".csv", ".xlsx"])
        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()

            # To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

            # To read file as string:
            string_data = stringio.read()

            # Can be used wherever a "file-like" object is accepted:
            st.session_state.input_df = pd.read_csv(
                uploaded_file,
                names=DATA_COLUMNS)

    with source_manual:
        with st.expander("Provide 10+ examples of ideal input outputs", expanded=False):
            st.session_state.manual_input_list = []
            st.session_state.manual_output_list = []
            # Loop through the current number of rows in the state
            for i in range(st.session_state.num_rows):
                col1, col2 = st.columns(2)
                with col1:
                    input_text = st.text_input(f"User Input {i + 1}")
                with col2:
                    output_text = st.text_input(f"AI Output {i + 1}")

                if (len(input_text) > 0) & (len(output_text) > 0):
                    st.session_state.manual_input_list.append(input_text)
                    st.session_state.manual_output_list.append(output_text)

            # "+" Button to add one more row
            if st.button('Add More'):
                st.session_state.num_rows += 1  # increase the number of rows by 1

            st.button(label='Validate input', use_container_width=True, on_click=validate_manual_input())

    with source_excel:
        st.markdown('File format not supported yet but hang on, we will be right back')
    with source_pdf:
        st.markdown('File format not supported yet but hang on, we will be right back')
    with source_word:
        st.markdown('File format not supported yet but hang on, we will be right back')


# Step 3

if (len(st.session_state.input_df) > 0) & (len(st.session_state.system_prompt) > 0):
    st.subheader("Step 3: Edit/ Validate your data", anchor="step-3")

    st.session_state.edited_df = st.data_editor(st.session_state.input_df, num_rows="dynamic", use_container_width=True)

    st.button(label='Export', use_container_width=True, on_click=validate_edited_df)

    # Step 4

    if len(st.session_state.valid_df) > 0:
        st.subheader("Step 4: Export formatted data for the chosen destination.")

        dest_openai, dest_other = st.tabs(["OpenAI fine-tuning", " "])

        with dest_openai:
            input_list = st.session_state.valid_df.iloc[:,0].tolist()
            output_list = st.session_state.valid_df.iloc[:,1].tolist()
            jsonl_str = format_for_openai_finetuning(st.session_state.system_prompt, input_list, output_list)

            if jsonl_str:
                jsonl_bytes = str.encode(jsonl_str)

                unique_id = f"l-{len(st.session_state.valid_df)}-h5{str(hash(jsonl_str))[:5]}"
                filename =f'openai-fine-tuning-{unique_id}.jsonl'

                st.markdown('Your data has been converted to the valid format for OpenAI finetuing API !')
                st.markdown(f'Download it as {filename}')
                st.download_button(
                    label="Download",
                    data=jsonl_bytes,
                    file_name=filename,
                    mime="text/jsonl",
                )
