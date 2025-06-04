import streamlit as st
import pandas as pd
import google.generativeai as genai
import os


genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Set up model
model = genai.GenerativeModel('gemini-1.5-flash')

# Streamlit UI
st.set_page_config(page_title="Feedback Summarizer", layout="centered")
st.title("User Feedback Summarizer")
st.markdown("Upload a CSV of user feedback or paste a list of feedback comments below. LLM will summarize it all.")

# Input option
upload = st.file_uploader("Upload CSV (must have a 'feedback' column)", type="csv")
text_input = st.text_area("Or paste multiple feedback comments here (one per line)", height=200)

feedback_list = []

# Process input
if upload:
    df = pd.read_csv(upload)
    if 'feedback' not in df.columns:
        st.error("CSV must have a 'feedback' column.")
    else:
        feedback_list = df['feedback'].dropna().tolist()
elif text_input:
    feedback_list = [line.strip() for line in text_input.splitlines() if line.strip()]

# Generate summary
if feedback_list and st.button("Summarize Feedback"):
    with st.spinner("Summarizing..."):
        prompt = f"""
You are an expert product analyst. Summarize the following {len(feedback_list)} pieces of user feedback:

{feedback_list}

Return the output in the following format:
- Overall Sentiment:
- Common Positive Feedback:
- Common Complaints:
- Suggestions:
- One-line Executive Summary:
"""

        try:
            response = model.generate_content(prompt)
            st.success("Summary generated!")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error from LLM: {e}")
else:
    st.info("Upload feedback or paste some to get started.")
