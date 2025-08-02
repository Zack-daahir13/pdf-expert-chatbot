import streamlit as st
from chatbot import get_chat_response
from utils import extract_text_from_pdf, summarize_text
from voice_module import record_and_transcribe, speak_text
import pandas as pd
import base64
import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="📘 PDF Expert Chatbot with Voice AI 🎙️", layout="wide")

st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
        }
        .stTextInput > div > div > input {
            background-color: #fff;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #ccc;
        }
        .stTextArea > div > textarea {
            background-color: #fff;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #ccc;
        }
        .css-1aumxhk {
            display: none;
        }
        footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📘 PDF Expert Chatbot with Voice AI 🎙️")

uploaded_file = st.file_uploader("📂 Upload your PDF file here", type=["pdf"])

if uploaded_file:
    with st.spinner("📖 Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("✅ PDF Loaded Successfully!")

    st.subheader("🧠 PDF Summary")
    summary = summarize_text(pdf_text)
    st.info(summary)

    st.text_area("📄 Extracted Text", value=pdf_text[:3000], height=200)

    st.subheader("💬 Ask your question:")
    user_input = st.text_input("Type or use voice 🎤")

    if st.button("🎙️ Record Voice"):
        st.info("Recording... Please speak")
        user_input = record_and_transcribe()
        st.success("🗣️ Transcribed: " + user_input)

    chat_history = []

    if user_input:
        with st.spinner("🤔 Generating response..."):
            answer = get_chat_response(user_input, pdf_text)
            st.success(answer)
            if st.button("🔊 Read Answer"):
                speak_text(answer)
            chat_history.append({"Question": user_input, "Answer": answer})

    if chat_history:
        df = pd.DataFrame(chat_history)
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown(f'<a href="data:file/csv;base64,{b64}" download="chat_history.csv" style="color:green;font-weight:bold;">📩 Download Chat History</a>', unsafe_allow_html=True)

st.markdown("""
---
<center>
    <div style='padding: 20px;'>
        <h4 style='color: #2E8B57;'>🔗 Made with ❤️ by <a href='mailto:zackdaahir909@gmail.com' style='color:#0066cc;'>Zack Daahir</a></h4>
        <p style='font-size:14px;'>
            Follow me on 
            <a href='https://github.com/Zack-daahir13' target='_blank' style='color:#333;'>GitHub</a> | 
            <a href='https://www.facebook.com/share/15gDe9dk1e/' target='_blank' style='color:#3b5998;'>Facebook</a> | 
            <a href='https://www.youtube.com/@zack-daahir' target='_blank' style='color:#c4302b;'>YouTube</a>
        </p>
    </div>
</center>
""", unsafe_allow_html=True)
