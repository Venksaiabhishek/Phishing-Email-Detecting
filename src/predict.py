import joblib
import os
import gdown
import numpy as np

# Define file IDs and associated metadata
MODEL_INFO = {
    "Logistic Regression": {
        "model_file": "logistic_regression.joblib",
        "acc": 97.85,
        "gdown_id": "1meRs6yHSv2qcTLo--i2-RImKQ_W1HbFY"
    },
    "Random Forest": {
        "model_file": "random_forest.joblib",
        "acc": 98.14,
        "gdown_id": "1oOp7i1lwb_HeF6lKuL_PEZ6oDuG9IZDd"
    },
    "Decision Tree": {
        "model_file": "decision_tree.joblib",
        "acc": 96.32,
        "gdown_id": "1ccYMFc9ib0TdVE-MP_qPJp3GpQnt749E"
    },
    "Naive Bayes": {
        "model_file": "naive_bayes.joblib",
        "acc": 95.67,
        "gdown_id": "1A4rokomiKU-ov_c2ssGeu6KECTv0_kml"
    },
    "Gradient Boosting": {
        "model_file": "gradient_boosting.joblib",
        "acc": 98.92,
        "gdown_id": "1ACnjQ4tGCYAL4SN7O7V8toBgz7veh9Pd"
    },
    "AdaBoost": {
        "model_file": "adaboost.joblib",
        "acc": 97.12,
        "gdown_id": "1zkJcP25AT0JhgqCqD1VlT3BizIWGAIo8"
    },
    "KNN": {
        "model_file": "knn.joblib",
        "acc": 94.88,
        "gdown_id": "1txMEoU7MkGizWvq89OPYN3q9asYFntoW"
    }
}

# TF-IDF Vectorizer info
VEC_FILE = "tfidf_vectorizer.joblib"
VEC_GDOWN_ID = "1kKUuP_Omp4fw-qSwO2c5o15dwF09Um3h"

def download_if_not_exists(file_name, file_id):
    if not os.path.exists(file_name):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, file_name, quiet=False)

# Load vectorizer
download_if_not_exists(VEC_FILE, VEC_GDOWN_ID)
vectorizer = joblib.load(VEC_FILE)

# Load models
models = {}
for model_name, info in MODEL_INFO.items():
    download_if_not_exists(info["model_file"], info["gdown_id"])
    models[model_name] = joblib.load(info["model_file"])

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

    final_pred = round(np.mean(votes))  # Majority vote
    final_label = "Phishing" if final_pred == 1 else "Legitimate"
    overall_acc = np.mean([info["acc"] for info in MODEL_INFO.values()])
    return final_label, overall_acc, predictions
