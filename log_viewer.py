import streamlit as st
import time
import os

# Page config
st.set_page_config(
    page_title="Orchestrator Logs",
    page_icon="📝",
    layout="wide"
)

# Title
st.title("📝 Multi-Agent Orchestrator Logs")

# Log file path
LOG_FILE = "logs/run.log"

# Check if log file exists
if not os.path.exists(LOG_FILE):
    st.error(f"⚠️ Log file not found at: `{LOG_FILE}`")
    st.info("Make sure you have run the orchestrator at least once.")
    st.stop()

# Auto-refresh control
col1, col2 = st.columns([1, 4])
with col1:
    auto_refresh = st.toggle('Auto-refresh logs', value=True)
with col2:
    if st.button('Clear Display'):
        placeholder = st.empty()

# Container for logs
log_container = st.empty()

def read_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading logs: {str(e)}"

# Main loop
while True:
    logs = read_logs()
    
    with log_container.container():
        # Display logs in a code block for better formatting
        st.code(logs, language="text")
        
        # Scroll to bottom hint (Streamlit doesn't strictly support auto-scroll yet without JS hacks)
        st.caption(f"Last updated: {time.strftime('%H:%M:%S')}")

    if not auto_refresh:
        break
        
    time.sleep(2)
