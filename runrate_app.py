import streamlit as st
import openai
import json
import os

# Set up OpenAI client using Streamlit secrets
client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

st.set_page_config(page_title="RunRate", layout="wide")
st.title("📊 RunRate: AI Financial Insights")

# Upload section
uploaded_file = st.file_uploader("Upload your monthly financial data (.json)", type="json")

if uploaded_file:
    financial_data = json.load(uploaded_file)

    st.subheader("✅ Financial Data Preview")
    st.json(financial_data)

    # GPT prompt structure
    messages = [
        {
            "role": "system",
            "content": "You are a professional FP&A analyst. Your job is to explain monthly financial performance in clear, helpful, non-jargon language. Provide 2–3 key insights."
        },
        {
            "role": "user",
            "content": f"Please analyze this financial data for {financial_data['month']}:\n```json\n{json.dumps(financial_data, indent=2)}\n```"
        }
    ]

    if st.button("💡 Generate AI Insight"):
        with st.spinner("Analyzing with GPT..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.3,
                max_tokens=500
            )

            insight = response.choices[0]()

