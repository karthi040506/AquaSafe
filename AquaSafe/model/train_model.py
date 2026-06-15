import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix

# 1. Load Data
print("Loading data...")
try:
    data = pd.read_csv('../data/Water_contamination.csv')
    print(f"Data shape: {data.shape}")
except FileNotFoundError:
    # Try absolute path or local run adjustment
    data = pd.read_csv('data/Water_contamination.csv')

# 2. Preprocessing
print("Preprocessing...")
if 'Region' in data.columns:
    data = data.drop(columns=['Region'])

# Features & Target
# Ensure column names match CSV exactly: Criteria, %percentage, Salt_Count
X = data[['Criteria', '%percentage', 'Salt_Count']]
y = data['Viability']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline Construction
categorical_features = ['Criteria']
numeric_features = ['%percentage', 'Salt_Count']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Model
clf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# 3. Training
print("Training model...")
clf.fit(X_train, y_train)

# 4. Evaluation
print("Evaluating...")
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print(f"Accuracy: {acc:.4f}")
print("Confusion Matrix:")
print(conf_matrix)

# 5. Save Model
print("Saving model...")
with open('trained_model.pkl', 'wb') as f:
    pickle.dump(clf, f)

print("Done. Model saved to model/trained_model.pkl (relative to execution)")
