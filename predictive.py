import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
import numpy as np

# --- Predictive Analytics (XGBoost) ---

# This is a highly simplified synthetic dataset for demonstration.
# In a real scenario, you'd have hundreds/thousands of patients and real features.
np.random.seed(42)
num_patients = 1000

data = {
    'latest_hba1c': np.random.uniform(5.0, 10.0, num_patients),
    'latest_cholesterol': np.random.uniform(150, 250, num_patients),
    'latest_bp_systolic': np.random.uniform(100, 180, num_patients),
    'latest_bp_diastolic': np.random.uniform(60, 110, num_patients),
    'age': np.random.randint(30, 80, num_patients),
    'has_diabetes': np.random.randint(0, 2, num_patients),
    'has_chest_pain_history': np.random.randint(0, 2, num_patients),
    'time_since_diabetes_years': np.random.uniform(0, 15, num_patients) * np.random.randint(0, 2, num_patients) # Only if has_diabetes
}
df_features = pd.DataFrame(data)

# Simulate a 'heart_attack_risk' target variable
# Higher HbA1c, cholesterol, BP, age, and diabetes/chest pain history increase risk
df_features['heart_attack_risk'] = (
    0.1 * df_features['latest_hba1c'] +
    0.05 * df_features['latest_cholesterol'] +
    0.08 * df_features['latest_bp_systolic'] +
    0.1 * df_features['age'] +
    2 * df_features['has_diabetes'] +
    1.5 * df_features['has_chest_pain_history'] +
    0.5 * df_features['time_since_diabetes_years'] +
    np.random.normal(0, 1, num_patients) # Add some noise
)
df_features['heart_attack_risk'] = (df_features['heart_attack_risk'] > df_features['heart_attack_risk'].median()).astype(int) # Binary classification

# Handle NaN created by `time_since_diabetes_years` where has_diabetes is 0
df_features['time_since_diabetes_years'] = df_features['time_since_diabetes_years'].fillna(0)


X = df_features.drop('heart_attack_risk', axis=1)
y = df_features['heart_attack_risk']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Initialize and train XGBoost classifier
model = xgb.XGBClassifier(objective='binary:logistic', eval_metric='logloss', use_label_encoder=False, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred_proba = model.predict_proba(X_test)[:, 1]
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f"\n--- XGBoost Model Performance (Synthetic Data) ---")
print(f"Accuracy: {accuracy:.4f}")
print(f"ROC AUC: {roc_auc:.4f}")
