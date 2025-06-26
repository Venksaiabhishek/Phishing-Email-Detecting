import joblib
import os

MODEL_NAMES = [
    "logistic_regression",
    "random_forest",
    "gradient_boosting",
    "naive_bayes",
    "svm"
]

def load_model_and_vectorizer(model_name):
    model_path = f"models/{model_name}.joblib"
    vect_path = "models/tfidf_vectorizer.joblib"
    if not os.path.exists(model_path) or not os.path.exists(vect_path):
        raise FileNotFoundError(f"Missing: {model_path} or {vect_path}")
    return joblib.load(model_path), joblib.load(vect_path)

def predict_email(email_text):
    """
    Returns predictions from all ML models as a dict: {Model Name -> 'Phishing'/'Legit'}
    """
    results = {}
    for name in MODEL_NAMES:
        model, vect = load_model_and_vectorizer(name)
        pred = model.predict(vect.transform([email_text]))[0]
        label = "Phishing" if pred == 1 else "Legit"
        results[name.replace("_", " ").title()] = label
    return results

# CLI test
if __name__ == "__main__":
    sample = "Your account has been suspended. Click http://fake-login.com"
    output = predict_email(sample)
    for m, l in output.items():
        print(f"{m:<20}: {l}")