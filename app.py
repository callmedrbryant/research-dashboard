import streamlit as st
import pandas as pd
import requests
import re

st.set_page_config(page_title="Deep Research Dashboard", layout="wide")
st.title("Research Dashboard MVP (AI-Powered by n8n)")

N8N_WEBHOOK_URL = "https://stardust-gemini.app.n8n.cloud/webhook/research"

topic = st.text_input("Enter research topic. Then trigger refresh.", "Computer hardware market")

if st.button("🔄 Trigger Agent Refresh"):
    with st.spinner("n8n Agent is scouring the web..."):
        try:
            response = requests.post(N8N_WEBHOOK_URL, json={"topic": topic})
            
            if response.status_code == 200:
                # Save the raw text response directly into memory
                st.session_state['raw_text'] = response.text
                st.success("Dashboard Refreshed with latest live research!")
            else:
                st.error(f"n8n error: Code {response.status_code}")
        except Exception as e:
            st.error(f"Could not connect to n8n: {e}")

# If we have data, render it cleanly
if 'raw_text' in st.session_state:
    raw_content = st.session_state['raw_text']
    
    st.header(f"Insights for: {topic}")
    
    # Render the AI's full written response beautifully
    st.subheader("📝 Executive Summary & Insights")
    st.info(raw_content)
    
    # Pull any percentages or numeric metrics out of the text automatically to build a table
    st.subheader("📊 Auto-Extracted Key Metrics")
    
    # Simple rule to find sentences containing statistics
    sentences = re.split(r'(?<=[.!?])\s+', raw_content)
    found_metrics = []
    
    for sentence in sentences:
        # Check if the sentence contains numbers, percentages, or market terms
        if any(char.isdigit() for char in sentence) or "%" in sentence or "market" in sentence.lower():
            if len(sentence.strip()) > 10:
                found_metrics.append({"Discovered Statistic / Insight": sentence.strip()})
                
    if found_metrics:
        df = pd.DataFrame(found_metrics)
        st.dataframe(df, use_container_width=True)
    else:
        st.write("No standalone metrics rows extracted yet.")
