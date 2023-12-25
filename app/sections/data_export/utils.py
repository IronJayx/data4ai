import streamlit as st


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
