import os
import joblib
import gdown
from collections import Counter

# Mapping of model names and their Drive file IDs
FILES = {
    "logistic_regression.joblib": "1meRs6yHSv2qcTLo--i2-RImKQ_W1HbFY",
    "random_forest.joblib": "1oOp7i1lwb_HeF6lKuL_PEZ6oDuG9IZDd",
    "xgboost.joblib": "1ccYMFc9ib0TdVE-MP_qPJp3GpQnt749E",
    "naive_bayes.joblib": "1A4rokomiKU-ov_c2ssGeu6KECTv0_kml",
    "svc.joblib": "1ACnjQ4tGCYAL4SN7O7V8toBgz7veh9Pd",
    "decision_tree.joblib": "1zkJcP25AT0JhgqCqD1VlT3BizIWGAIo8",
    "knn.joblib": "1txMEoU7MkGizWvq89OPYN3q9asYFntoW",
    "tfidf_vectorizer.joblib": "1kKUuP_Omp4fw-qSwO2c5o15dwF09Um3h"
}

def download_if_missing(file, file_id):
    if not os.path.exists(f"models/{file}"):
        os.makedirs("models", exist_ok=True)
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, f"models/{file}", quiet=False)

# Download all files
for file, file_id in FILES.items():
    download_if_missing(file, file_id)

# Load vectorizer
vectorizer = joblib.load("models/tfidf_vectorizer.joblib")

# Load all models
models = {
    name.replace(".joblib", ""): joblib.load(f"models/{name}")
    for name in FILES
    if name != "tfidf_vectorizer.joblib"
}

def predict_email(email_text):
    X = vectorizer.transform([email_text])
    preds = []

    for model_name, model in models.items():
        pred = model.predict(X)[0]
        preds.append(pred)

    # Majority vote
    final_pred = Counter(preds).most_common(1)[0][0]
    confidence = round((preds.count(final_pred) / len(preds)) * 100, 2)
    label = "Phishing" if final_pred == 1 else "Legitimate"

    return {
        "label": label,
        "confidence": f"{confidence}%"
    }
