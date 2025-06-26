import streamlit as st
import sys
import os

# Ensure the `src` folder is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.predict_transformer import predict_transformer

st.set_page_config(page_title="Phishing Detector", page_icon="📧")
st.title("📧 Phishing Email Detector")

email_input = st.text_area("Paste an email below to check if it's phishing:")

if st.button("Analyze"):
    if not email_input.strip():
        st.warning("Please paste some email content before analyzing.")
    else:
        st.subheader("🤖 Transformer Model Prediction")
        try:
            result = predict_transformer(email_input)
            label = max(result, key=result.get)
            confidence = result[label] * 100

            # Highlight the prediction
            st.markdown(
                f"<h2 style='color:{"red" if label == "phishing" else "green"};'>Prediction: {label.upper()}</h2>",
                unsafe_allow_html=True
            )
            st.markdown(f"**Confidence:** {confidence:.2f}%")

            # Optional visual cue
            if label == "phishing":
                st.error("⚠️ This email is likely a phishing attempt.")
            else:
                st.success("✅ This email appears to be legitimate.")
        except Exception as e:
            st.error(f"Error with transformer model: {e}")
