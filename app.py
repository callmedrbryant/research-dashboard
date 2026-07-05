import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="Deep Research Dashboard", layout="wide")
st.title("🤖 Live AI Research Dashboard (Powered by n8n)")

# Your live n8n URL
N8N_WEBHOOK_URL = "https://n8n.cloud"

topic = st.text_input("Enter research topic:", "Solid state battery market")

if st.button("🔄 Trigger Agent Refresh"):
    with st.spinner("n8n Agent is scouring the web..."):
        try:
            response = requests.post(N8N_WEBHOOK_URL, json={"topic": topic})
            
            if response.status_code == 200:
                # Try parsing as JSON first
                try:
                    st.session_state['report'] = response.json()
                    st.success("Dashboard Refreshed successfully as structured data!")
                except Exception:
                    # If it's a raw string or text block, store it safely as text
                    st.session_state['report'] = {"topic": topic, "summary": response.text, "key_metrics": []}
                    st.warning("n8n returned unstructured text instead of a JSON table.")
            else:
                st.error(f"n8n error: Code {response.status_code}")
        except Exception as e:
            st.error(f"Could not connect to n8n: {e}")

# Render data on screen based on what n8n sent back
if 'report' in st.session_state:
    report = st.session_state['report']
    st.header(f"Insights for: {report.get('topic', topic)}")
    
    st.subheader("📝 Summary / Raw Response")
    st.write(report.get('summary', 'No summary text returned.'))
    
    st.subheader("📊 Key Extracted Metrics Table")
    metrics = report.get('key_metrics', [])
    
    # If the response was a string containing nested JSON, try to clean it
    if isinstance(metrics, str):
        try:
            metrics = json.loads(metrics)
        except:
            pass
            
    if isinstance(metrics, list) and len(metrics) > 0:
        df = pd.DataFrame(metrics)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No data rows found. Check the text box above to see the AI's full written answer.")
