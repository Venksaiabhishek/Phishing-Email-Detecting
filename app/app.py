import streamlit as st
import sys
import os

# Ensure the `src` folder is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.predict import predict_email
from src.predict_transformer import predict_transformer

st.set_page_config(page_title="Phishing Detector", page_icon="📧")
st.title("📧 Phishing Email Detector")

email_input = st.text_area("Paste an email below to check if it's phishing:")

if st.button("Analyze"):
    if not email_input.strip():
        st.warning("Please paste some email content before analyzing.")
    else:
        st.subheader("🔍 Final ML Prediction")
        try:
            result = predict_email(email_input)
            st.write(f"**Prediction:** {result['label']}")
            st.write(f"**Confidence:** {result['confidence']}")
        except Exception as e:
            st.error(f"Error with ML models: {e}")

        st.subheader("🤖 Transformer Model Prediction")
        try:
            trans_pred = predict_transformer(email_input)
            label = max(trans_pred, key=trans_pred.get)
            confidence = round(trans_pred[label] * 100, 2)
            st.write(f"**Prediction:** {label.capitalize()}")
            st.write(f"**Confidence:** {confidence}%")
        except Exception as e:
            st.error(f"Error with transformer model: {e}")
