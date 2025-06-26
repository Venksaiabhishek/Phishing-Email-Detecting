# src/train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# 1. Load cleaned dataset
DATA_PATH = "data/processed/emails_hf_clean.csv"
df = pd.read_csv(DATA_PATH)

# 2. Split data
X = df['text']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Vectorize text
vectorizer = TfidfVectorizer(max_features=10000, stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 4. Train model

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=100),
    "Gradient Boosting": GradientBoostingClassifier(),
    "Naive Bayes": MultinomialNB(),
    "SVM": SVC()
}
# 5. Train, Evaluate, Save
for name, model in models.items():
    model.fit(X_train_tfidf, y_train)  # ✅ Use TF-IDF features here
    y_pred = model.predict(X_test_tfidf)  # ✅ Predict on TF-IDF test features
    print(f"📊 Model: {name}")
    print(classification_report(y_test, y_pred))

    # Save model and vectorizer
    joblib.dump(model, f"models/{name.replace(' ', '_').lower()}.joblib")

# Save vectorizer once
joblib.dump(vectorizer, "models/tfidf_vectorizer.joblib")