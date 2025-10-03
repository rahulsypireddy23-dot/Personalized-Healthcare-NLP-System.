import shap
import matplotlib.pyplot as plt

# --- Explainable AI (SHAP) ---

# Create a SHAP explainer object
explainer = shap.TreeExplainer(model)

# Calculate SHAP values for the test set
shap_values = explainer.shap_values(X_test)

print("\n--- SHAP Explanations ---")

# Plotting overall feature importance (mean absolute SHAP value)
# plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values, X_test, plot_type="bar", show=False)
plt.title("Overall Feature Importance (Mean |SHAP value|)")
plt.tight_layout()
# plt.show()
print("Overall Feature Importance plot generated.")
# For visualization purposes, I'll generate an image of the summary plot: 
# plt.savefig("overall_feature_importance.png")

# Plotting individual prediction explanation (force plot)
# This shows how each feature contributes to a single prediction
sample_idx = 0 # Explain the first sample in the test set
print(f"\nExplaining prediction for sample {sample_idx} (True label: {y_test.iloc[sample_idx]})")
# plt.figure(figsize=(12, 4))
shap.force_plot(explainer.expected_value, shap_values[sample_idx,:], X_test.iloc[sample_idx,:], show=False, matplotlib=True)
plt.title(f"Individual Prediction Explanation for Sample {sample_idx}")
plt.tight_layout()
# plt.show()
print("Individual Prediction Explanation (Force Plot) generated.")
# For visualization purposes, I'll generate an image of the force plot: 
# plt.savefig("individual_prediction_explanation.png")
