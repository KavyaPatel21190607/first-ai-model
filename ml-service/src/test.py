import pickle
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

DATA_PATH = "../data/spam_ham_dataset.csv"
MODEL_PATH = "../models/spam_classifier.pkl"
VECTORIZER_PATH = "../models/vectorizer.pkl"

df = pd.read_csv(DATA_PATH)

TEXT_COLUMN = "text"
LABEL_COLUMN = "label"

# ✅ FIX: Map labels to numbers
label_map = {"ham": 0, "spam": 1}
df[LABEL_COLUMN] = df[LABEL_COLUMN].map(label_map)

X = df[TEXT_COLUMN]
y = df[LABEL_COLUMN]

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

X_vec = vectorizer.transform(X)
y_pred = model.predict(X_vec)

print("Accuracy:", accuracy_score(y, y_pred))
print("Precision:", precision_score(y, y_pred))
print("Recall:", recall_score(y, y_pred))
print("F1:", f1_score(y, y_pred))

print("\nConfusion Matrix:\n", confusion_matrix(y, y_pred))
print("\nClassification Report:\n", classification_report(y, y_pred, target_names=["ham", "spam"]))
