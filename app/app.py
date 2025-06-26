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
        st.subheader("🔍 ML Model Predictions")
        try:
            ml_preds = predict_email(email_input)
            for model, label in ml_preds.items():
                st.write(f"**{model}**: {label}")
        except Exception as e:
            st.error(f"Error with ML models: {e}")

        st.subheader("🤖 Transformer Model Prediction")
        try:
            trans_pred = predict_transformer(email_input)
            st.json(trans_pred)
        except Exception as e:
            st.error(f"Error with transformer model: {e}")

##IF DOING LOCALLY UNCOMMENT THE BELOW COMMENTED AND COMMENT THE ABOVE CODE, as ML models are not available in online

#import streamlit as st
#import sys
#import os

# Ensure the `src` folder is importable by adding project root to sys.path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#from src.predict import predict_email
#from src.predict_transformer import predict_transformer  # if present

#st.set_page_config(page_title="Phishing Detector", page_icon="📧")
#st.title("📧 Phishing Email Detector")

#email_input = st.text_area("Paste an email below to check if it's phishing:")

#if st.button("Analyze"):
    #if not email_input.strip():
       # st.warning("Please paste some email content before analyzing.")
    #else:
       # st.subheader("🔍 ML Model Predictions")
        #try:
          #  ml_preds = predict_email(email_input)
           # for model, label in ml_preds.items():
          #      st.write(f"**{model}**: {label}")
       # except Exception as e:
        #    st.error(f"Error with ML models: {e}")

      #  st.subheader("🤖 Transformer Model Prediction")
       # try:
          #  trans_pred = predict_transformer(email_input)
          #  st.json(trans_pred)
       # except Exception as e:
      #      st.error(f"Error with transformer model: {e}")
