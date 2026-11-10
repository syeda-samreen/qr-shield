import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

data = pd.read_csv("features.csv")
X = data.drop(columns="label")
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=100, random_state=42, n_jobs=-1, class_weight="balanced"
)
model.fit(X_train, y_train)

pred = model.predict(X_test)
print(classification_report(y_test, pred, target_names=["good", "bad"]))
print("Confusion matrix:")
print(confusion_matrix(y_test, pred))
print()

importances = pd.Series(model.feature_importances_, index=X.columns)
print(importances.sort_values(ascending=False))

joblib.dump(model, "model.joblib")
