# src/predict_transformer.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "cybersectony/phishing-email-detection-distilbert_v2.4.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.eval()

def predict_transformer(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=-1).tolist()[0]
    return {"legitimate": probs[0], "phishing": probs[1]}