import joblib
from sklearn.metrics import accuracy_score

print("Loading savedmodel.pth...")
model, X_test, y_test = joblib.load("savedmodel.pth")

preds = model.predict(X_test)
accuracy = accuracy_score(y_test, preds) * 100
print("=============================================")
print(f"  Test Accuracy: {accuracy:.2f}%")
print("=============================================")