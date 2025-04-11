import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
import pandas as pd
from backend.utils.db import get_user_history as fetch_user_history

from components.navbar import show_navbar
from components.sidebar import show_sidebar

# Set page config
st.set_page_config(page_title="SQLMate History", page_icon="🕒")

# Show UI components
show_sidebar()
show_navbar()

st.title("🕒 Your Chat History")

# Check if user is logged in
if "username" not in st.session_state:
    st.warning("⚠️ Please log in to view your chat history.")
    st.stop()

# Fetch user chat history
history = fetch_user_history(st.session_state["username"])

# Display chat history
if not history:
    st.info("You don't have any chat history yet. Ask something in the Chat tab!")
else:
    for i, (question, answer, timestamp) in enumerate(history):
        with st.expander(f"🗨️ {question[:50]}..."):
            st.markdown(f"**Q:** {question}")
            st.markdown(f"**A:** {answer}")
            st.caption(f"🕒 {timestamp}")

    # Download chat history as CSV
    df = pd.DataFrame(history, columns=["Question", "Answer", "Timestamp"])
    if st.download_button(
        label="📥 Download History as CSV",
        data=df.to_csv(index=False),
        file_name="sqlmate_chat_history.csv",
        mime="text/csv"
    ):
        st.success("Downloaded your chat history!")

