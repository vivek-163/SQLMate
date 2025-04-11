# import streamlit as st
# from langchain.agents import create_sql_agent
# from langchain.sql_database import SQLDatabase
# from langchain.agents.agent_types import AgentType
# from langchain.callbacks import StreamlitCallbackHandler
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
# from sqlalchemy import create_engine
# from langchain_groq import ChatGroq

# st.set_page_config(page_title="SQLMate - Chat with MySQL", page_icon="🦜")
# st.title("🦜 SQLMate: Chat with MySQL Database")

# # Initialize session state for database connection & API key
# if "mysql_host" not in st.session_state:
#     st.session_state["mysql_host"] = ""
# if "mysql_user" not in st.session_state:
#     st.session_state["mysql_user"] = ""
# if "mysql_password" not in st.session_state:
#     st.session_state["mysql_password"] = ""
# if "mysql_db" not in st.session_state:
#     st.session_state["mysql_db"] = ""
# if "api_key" not in st.session_state:
#     st.session_state["api_key"] = ""

# # Sidebar inputs for MySQL connection (stored in session state)
# st.sidebar.subheader("MySQL Database Connection")
# st.session_state["mysql_host"] = st.sidebar.text_input("MySQL Host (e.g., localhost)", st.session_state["mysql_host"])
# st.session_state["mysql_user"] = st.sidebar.text_input("MySQL User", st.session_state["mysql_user"])
# st.session_state["mysql_password"] = st.sidebar.text_input("MySQL Password", type="password", value=st.session_state["mysql_password"])
# st.session_state["mysql_db"] = st.sidebar.text_input("MySQL Database Name", st.session_state["mysql_db"])

# # API Key input (stored in session state)
# st.session_state["api_key"] = st.sidebar.text_input("Groq API Key", type="password", value=st.session_state["api_key"])

# # Validate input fields
# if not (st.session_state["mysql_host"] and st.session_state["mysql_user"] and st.session_state["mysql_password"] and st.session_state["mysql_db"]):
#     st.info("Please enter all MySQL credentials to proceed.")
#     st.stop()

# if not st.session_state["api_key"]:
#     st.info("Please enter your Groq API Key.")
#     st.stop()

# # Create MySQL connection
# def configure_db():
#     return SQLDatabase(create_engine(f"mysql+mysqlconnector://{st.session_state['mysql_user']}:{st.session_state['mysql_password']}@{st.session_state['mysql_host']}/{st.session_state['mysql_db']}"))

# db = configure_db()

# # LLM setup
# llm = ChatGroq(groq_api_key=st.session_state["api_key"], model_name="Llama3-8b-8192", streaming=True)

# # Toolkit setup
# toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# # Agent setup
# agent = create_sql_agent(
#     llm=llm,
#     toolkit=toolkit,
#     verbose=True,
#     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
# )

# # Retain session history
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I assist you?"}]

# # Clear chat history button
# if st.sidebar.button("Clear Chat History"):
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I assist you?"}]
#     st.rerun()

# # Display chat history
# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# # User input field
# user_query = st.chat_input(placeholder="Ask your SQL Database anything...")

# if user_query:
#     st.session_state.messages.append({"role": "user", "content": user_query})
#     st.chat_message("user").write(user_query)

#     with st.chat_message("assistant"):
#         streamlit_callback = StreamlitCallbackHandler(st.container())
#         try:
#             response = agent.run(user_query, callbacks=[streamlit_callback])
#             st.session_state.messages.append({"role": "assistant", "content": response})
#             st.write(response)
#         except Exception as e:
#             st.error(f"❌ Error processing query: {e}")



import streamlit as st

st.set_page_config(page_title="SQLMate", page_icon="🧠", layout="wide")

from components.navbar import show_navbar
from components.sidebar import show_sidebar

# Sidebar & Navbar
show_sidebar()
show_navbar()

# --- Custom CSS ---
light_bg = """
    background: linear-gradient(135deg, #c2f0ff, #e6fff5);
"""
sidebar_style = """
    background: linear-gradient(135deg, #d4f1ff, #a6e3ff);
    padding: 1rem;
    border-radius: 10px;
"""

st.markdown(f"""
    <style>
        .stApp {{
            {light_bg}
            background-attachment: fixed;
        }}

        .glass-card {{
            background: rgba(255, 255, 255, 0.25);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
            color: #000;
        }}

        .glass-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }}

        .glass-card ul {{
            padding-left: 1.5rem;
            list-style-type: disc;
        }}

        /* Sticky navbar */
        .navbar {{
            position: sticky;
            top: 0;
            z-index: 999;
        }}

        /* Sidebar animation + background */
        section[data-testid="stSidebar"] > div:first-child {{
            transition: all 0.3s ease-in-out;
            {sidebar_style}
        }}
        section[data-testid="stSidebar"]:hover > div:first-child {{
            transform: scale(1.03);
            box-shadow: 0 0 15px rgba(0, 191, 255, 0.3);
        }}

        .cta-button {{
            text-align: center;
            margin-top: 1rem;
        }}
    </style>
""", unsafe_allow_html=True)

# ----------------- CONTENT ------------------ #

st.markdown("""
<div class="glass-card">
    <div class="glass-title">📖 About SQLMate</div>
    <p>SQLMate is your intelligent companion to interact with MySQL databases using natural language.
    Whether you're a developer, analyst, or just someone exploring SQL, SQLMate makes data access
    simple and intuitive.</p>
    <ul>
        <li>Connect to your own MySQL database</li>
        <li>Chat with your data in natural language</li>
        <li>View and download chat history</li>
        <li>Securely register and log in</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown('''
<div class="glass-card">
    <div class="glass-title">⚙️ How It Works</div>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div style="text-align: center; flex: 1; min-width: 200px;">
            <img src="https://cdn-icons-png.flaticon.com/512/3523/3523885.png" width="80"/>
            <p><strong>1. Connect your Database</strong></p>
            <p style="font-size: 0.9rem;">Securely connect to your MySQL database.</p>
        </div>
        <div style="text-align: center; flex: 1; min-width: 200px;">
            <img src="https://cdn-icons-png.flaticon.com/512/3649/3649463.png" width="80"/>
            <p><strong>2. Ask Questions in Plain English</strong></p>
            <p style="font-size: 0.9rem;">Type natural language queries like 'Show top 5 customers'.</p>
        </div>
        <div style="text-align: center; flex: 1; min-width: 200px;">
            <img src="https://cdn-icons-png.flaticon.com/512/4149/4149650.png" width="80"/>
            <p><strong>3. Get Results Instantly</strong></p>
            <p style="font-size: 0.9rem;">SQLMate translates it, executes, and shows results.</p>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<div class="glass-card">
    <div class="glass-title">✨ Key Features</div>
    <ul>
        <li>💬 <strong>Natural Language to SQL</strong></li>
        <li>🧠 <strong>Powered by LLM (Groq API)</strong></li>
        <li>💾 <strong>Chat History & Download Support</strong></li>
        <li>🔐 <strong>Secure Login & MySQL Integration</strong></li>
        <li>⚡ <strong>Fast & Intuitive Interface</strong></li>
    </ul>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<div class="glass-card">
    <div class="glass-title">🔑 How to Get Your Own Groq API Key</div>
    <p>To power natural language processing, SQLMate uses the Groq API with LLMs. You’ll need your own API key to start querying.</p>
    <ul>
        <li>Visit <a href="https://console.groq.com/keys" target="_blank">Groq Console</a>.</li>
        <li>Log in or create an account.</li>
        <li>Navigate to the <strong>API Keys</strong> section.</li>
        <li>Click on <strong>Create API Key</strong> and copy it.</li>
        <li>Paste the key when prompted in the Chat interface.</li>
    </ul>
    <p style="font-size: 0.9rem;"><em>Your API key stays only in your current session for privacy and security.</em></p>
</div>
''', unsafe_allow_html=True)

st.markdown('''
    <div class="glass-card" style="text-align: center;">
        <h3>🚀 Ready to try it out?</h3>
    </div>
''', unsafe_allow_html=True)

# Center button
st.markdown('<div class="cta-button">', unsafe_allow_html=True)
center1, center2, center3 = st.columns([1, 1, 1])
with center2:
    if st.button("Start Chatting Now", use_container_width=True):
        st.switch_page("pages/chat.py")
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit, FastAPI, and LangChain.")






