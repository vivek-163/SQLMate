 
# import streamlit as st
# import requests

# st.title("💬 Chat with SQL Database")

# # Check if database is connected
# if "db_credentials" not in st.session_state:
#     st.warning("⚠️ Please connect to a MySQL database from the main page.")
#     st.stop()

# # Get MySQL credentials from session state
# db_credentials = st.session_state["db_credentials"]

# # Chat input field
# user_query = st.text_input("Ask something from the database:")

# if st.button("Send"):
#     if not user_query:
#         st.error("❌ Please enter a query before sending.")
#     else:
#         # Send query to backend
#         response = requests.post(
#             "http://127.0.0.1:8000/chat",
#             json={"query": user_query, "db_credentials": db_credentials},
#         )

#         if response.status_code == 200:
#             result = response.json().get("result", "No response")
#             st.success("✅ Query executed successfully!")
#             st.write(result)
#         else:
#             st.error(f"❌ Error {response.status_code}: Unable to fetch response.")

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import streamlit as st
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
import pandas as pd
import re

from components.navbar import show_navbar
from components.sidebar import show_sidebar
from backend.utils.db import save_chat  # ✅

st.set_page_config(page_title="SQLMate Chat", page_icon="💬")
show_sidebar()
show_navbar()

st.title("💬 Chat with SQLMate")

# Initialize session state
for key in ["mysql_host", "mysql_user", "mysql_password", "mysql_db", "api_key"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# Sidebar inputs
st.sidebar.subheader("MySQL Database Connection")
st.session_state["mysql_host"] = st.sidebar.text_input("MySQL Host", st.session_state["mysql_host"])
st.session_state["mysql_user"] = st.sidebar.text_input("MySQL User", st.session_state["mysql_user"])
st.session_state["mysql_password"] = st.sidebar.text_input("MySQL Password", type="password", value=st.session_state["mysql_password"])
st.session_state["mysql_db"] = st.sidebar.text_input("MySQL Database Name", st.session_state["mysql_db"])
st.session_state["api_key"] = st.sidebar.text_input("Groq API Key", type="password", value=st.session_state["api_key"])

if not all([st.session_state[k] for k in ["mysql_host", "mysql_user", "mysql_password", "mysql_db"]]):
    st.info("Please enter all MySQL credentials to proceed.")
    st.stop()
if not st.session_state["api_key"]:
    st.info("Please enter your Groq API Key.")
    st.stop()

# Connect database
def configure_db():
    return SQLDatabase(create_engine(
        f"mysql+mysqlconnector://{st.session_state['mysql_user']}:{st.session_state['mysql_password']}@{st.session_state['mysql_host']}/{st.session_state['mysql_db']}"
    ))

db = configure_db()

llm = ChatGroq(groq_api_key=st.session_state["api_key"], model_name="Llama3-8b-8192", streaming=True)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I assist you?"}]
if "cleaned_history" not in st.session_state:
    st.session_state["cleaned_history"] = []

# Clear chat
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I assist you?"}]
    st.session_state["cleaned_history"] = []
    st.rerun()

# Display chat messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_query = st.chat_input(placeholder="Ask your SQL Database anything...")

def render_response(raw_response):
    if isinstance(raw_response, str):
        if "-" in raw_response and any(char.isdigit() for char in raw_response):
            parts = re.split(r'\s*(?<=\d{5,}\.?\d*)[,|\n]?\s*', raw_response.strip())
            parts = [p.strip() for p in parts if p.strip()]
            formatted = "\n".join([f"{i+1}. {line}" for i, line in enumerate(parts)])
            st.markdown(formatted)
            return formatted

        if "SELECT" in raw_response.upper() and "FROM" in raw_response.upper():
            st.code(raw_response.strip(), language="sql")
            return raw_response.strip()

        try:
            df = pd.read_csv(pd.compat.StringIO(raw_response))
            st.dataframe(df)
            return "Rendered as table"
        except:
            st.markdown(raw_response.strip())
            return raw_response.strip()
    else:
        st.markdown("🤔 Couldn't parse response properly.")
        return str(raw_response)

# On user query
if user_query:
    st.session_state["messages"].append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        try:
            response = agent.run(
                input=user_query,
                callbacks=[streamlit_callback],
                handle_parsing_errors=True
            )
            cleaned = render_response(response)
            st.session_state["messages"].append({"role": "assistant", "content": cleaned})
            st.session_state["cleaned_history"].append({"Q": user_query, "A": cleaned})

            # ✅ Save chat to DB if user is logged in
            if "username" in st.session_state:
                save_chat(st.session_state["username"], user_query, cleaned)

        except Exception as e:
            error_msg = f"❌ Error: {e}"
            st.error(error_msg)
            st.session_state["messages"].append({"role": "assistant", "content": error_msg})

# Option to export chat
if st.sidebar.download_button("📥 Download Chat", data=pd.DataFrame(st.session_state["cleaned_history"]).to_csv(index=False), file_name="sqlmate_chat_history.csv", mime="text/csv"):
    st.sidebar.success("Downloaded chat history!")
