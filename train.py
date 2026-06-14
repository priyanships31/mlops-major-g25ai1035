from sklearn.datasets import fetch_olivetti_faces
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib

print("Loading Olivetti faces dataset...")
data = fetch_olivetti_faces()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

model = DecisionTreeClassifier(random_state=42)

model.fit(X_train, y_train)

joblib.dump((model, X_test, y_test), "savedmodel.pth")
print("Model saved successfully as savedmodel.pth!")