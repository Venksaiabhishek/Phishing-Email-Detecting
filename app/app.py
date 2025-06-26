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
        try:
            final_label, overall_acc, model_preds = predict_email(email_input)
            st.subheader("🔍 Final ML Prediction")
            st.write(f"Prediction: **{final_label}**")
            st.write(f"Accuracy: **{overall_acc:.2f}%**")

            if st.button("Show model-wise predictions and accuracy"):
                for model_name, (pred, acc) in model_preds.items():
                    st.write(f"- **{model_name}** ➜ {pred} (Accuracy: {acc:.2f}%)")

        except Exception as e:
            st.error(f"Error with ML models: {e}")

        st.subheader("🤖 Transformer Model Prediction")
        try:
            trans_pred = predict_transformer(email_input)
            label = max(trans_pred, key=trans_pred.get)
            confidence = trans_pred[label] * 100
            st.write(f"Prediction: **{label.capitalize()}**")
            st.write(f"Confidence: **{confidence:.2f}%**")
        except Exception as e:
            st.error(f"Error with transformer model: {e}")
