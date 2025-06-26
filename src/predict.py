import joblib
import os
import numpy as np
import gdown

# Google Drive IDs
MODEL_FILES = {
    "Logistic Regression": "1meRs6yHSv2qcTLo--i2-RImKQ_W1HbFY",
    "Naive Bayes": "1oOp7i1lwb_HeF6lKuL_PEZ6oDuG9IZDd",
    "Random Forest": "1ccYMFc9ib0TdVE-MP_qPJp3GpQnt749E",
    "SVM": "1A4rokomiKU-ov_c2ssGeu6KECTv0_kml",
    "XGBoost": "1ACnjQ4tGCYAL4SN7O7V8toBgz7veh9Pd",
    "KNN": "1zkJcP25AT0JhgqCqD1VlT3BizIWGAIo8",
    "Decision Tree": "1txMEoU7MkGizWvq89OPYN3q9asYFntoW",
    "Gradient Boosting": "1kKUuP_Omp4fw-qSwO2c5o15dwF09Um3h"
}
VEC_FILE = "tfidf_vectorizer.joblib"
VEC_ID = "1Wtv5O1o6GfNU2Z7gAIGMCVkk_QI3Du0A"

MODEL_INFO = {
    "Logistic Regression": {"acc": 0.94},
    "Naive Bayes": {"acc": 0.92},
    "Random Forest": {"acc": 0.95},
    "SVM": {"acc": 0.93},
    "XGBoost": {"acc": 0.96},
    "KNN": {"acc": 0.88},
    "Decision Tree": {"acc": 0.91},
    "Gradient Boosting": {"acc": 0.95}
}

def download_if_not_exists(file_name, file_id):
    if not os.path.exists(file_name):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, file_name, quiet=False)

# Load vectorizer
download_if_not_exists(VEC_FILE, VEC_ID)
vectorizer = joblib.load(VEC_FILE)

# Load models
models = {}
for name, file_id in MODEL_FILES.items():
    file_path = f"{name.replace(' ', '_').lower()}.joblib"
    download_if_not_exists(file_path, file_id)
    models[name] = joblib.load(file_path)

def predict_email(text):
    X = vectorizer.transform([text])
    predictions = {}
    votes = []

    for model_name, clf in models.items():
        pred = clf.predict(X)[0]
        label = "Phishing" if pred == 1 else "Legitimate"
        acc = MODEL_INFO[model_name]["acc"]
        predictions[model_name] = (label, acc)
        votes.append(pred)

    final_pred = round(np.mean(votes))
    final_label = "Phishing" if final_pred == 1 else "Legitimate"
    overall_acc = np.mean([info["acc"] for info in MODEL_INFO.values()])

    return final_label, overall_acc, predictions
