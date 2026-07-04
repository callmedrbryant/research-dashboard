import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Deep Research Dashboard", layout="wide")
st.title("🤖 Live AI Research Dashboard (Powered by n8n)")

# ⚠️ WE WILL CHANGE THIS URL LATER ONCE YOUR N8N WORKFLOW IS READY
N8N_WEBHOOK_URL = "https://n8n.cloud"

topic = st.text_input("Enter research topic:", "Solid state battery market")

if st.button("🔄 Trigger Agent Refresh"):
    with st.spinner("n8n Agent is scouring the web..."):
        try:
            response = requests.post(N8N_WEBHOOK_URL, json={"topic": topic})
            if response.status_code == 200:
                st.session_state['report'] = response.json()
                st.success("Dashboard Refreshed!")
            else:
                st.error(f"n8n error: Code {response.status_code}")
        except Exception as e:
            st.error(f"Could not connect to n8n: {e}")

if 'report' in st.session_state:
    report = st.session_state['report']
    st.header(f"Insights for: {report.get('topic', topic)}")
    st.subheader("📝 Executive Summary")
    st.write(report.get('summary', 'No summary provided.'))
    
    st.subheader("📊 Key Extracted Metrics")
    df = pd.DataFrame(report.get('key_metrics', []))
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No structured metrics found for this topic yet.")
