import pandas as pd
import joblib
import os

# Load vectorizer
vectorizer = joblib.load("models/tfidf_vectorizer.joblib")

# Load models
model_paths = {
    "Logistic Regression": "models/logistic_regression.joblib",
    "Random Forest": "models/random_forest.joblib",
    "Gradient Boosting": "models/gradient_boosting.joblib",
    "Naive Bayes": "models/naive_bayes.joblib",
    "SVM": "models/svm.joblib",
}

models = {name: joblib.load(path) for name, path in model_paths.items()}

# Load test CSV
df = pd.read_csv("data/raw/real_world_emails.csv")
texts = df["text"]
X_tfidf = vectorizer.transform(texts)

# Predict
results = df.copy()
for name, model in models.items():
    predictions = model.predict(X_tfidf)
    results[name] = ["Phishing" if p == 1 else "Legit" for p in predictions]

# Save output
results.to_csv("data/predictions_output.csv", index=False)
print("✅ Predictions saved to data/predictions_output.csv")