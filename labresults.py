# --- Multi-Modal Integration (Conceptual) ---

# Example structured data (could come from a database)
lab_results = pd.DataFrame([
    {"patient_id": "P001", "date": "2020-01-20", "test": "HbA1c", "value": 7.2, "unit": "%"},
    {"patient_id": "P001", "date": "2021-03-15", "test": "Cholesterol", "value": 220, "unit": "mg/dL"},
    {"patient_id": "P001", "date": "2023-05-22", "test": "HbA1c", "value": 6.8, "unit": "%"}
])

vitals = pd.DataFrame([
    {"patient_id": "P001", "date": "2020-01-15", "bp_systolic": 140, "bp_diastolic": 90, "heart_rate": 85},
    {"patient_id": "P001", "date": "2023-05-20", "bp_systolic": 130, "bp_diastolic": 80, "heart_rate": 78}
])

# For a given patient and a prediction point in time, you'd aggregate these.
# Let's say we want features for patient P001 up to "2023-05-20"

def get_features_for_patient(patient_id, prediction_date):
    pred_dt = datetime.strptime(prediction_date, "%Y-%m-%d")

    # NLP features (from our earlier examples, simplified)
    # In a real system, you'd process all notes up to pred_dt
    nlp_features = {
        "has_diabetes": 1 if calculate_time_since_diagnosis(patient_df, "Diabetes") is not None else 0,
        "time_since_diabetes_years": calculate_time_since_diagnosis(patient_df, "Diabetes"),
        "has_chest_pain_history": 1 if any("chest pain" in e['entity_text'].lower()
                                            for idx, e in patient_df[patient_df['date'] <= pred_dt].iterrows()) else 0,
        # ... many more NLP-derived features
    }

    # Lab results (most recent before prediction_date)
    recent_labs = lab_results[(lab_results['patient_id'] == patient_id) &
                              (pd.to_datetime(lab_results['date']) <= pred_dt)]
    latest_hba1c = recent_labs[recent_labs['test'] == 'HbA1c'].sort_values(by='date', ascending=False).iloc[0]['value'] if not recent_labs[recent_labs['test'] == 'HbA1c'].empty else None
    latest_cholesterol = recent_labs[recent_labs['test'] == 'Cholesterol'].sort_values(by='date', ascending=False).iloc[0]['value'] if not recent_labs[recent_labs['test'] == 'Cholesterol'].empty else None

    # Vitals (most recent before prediction_date)
    recent_vitals = vitals[(vitals['patient_id'] == patient_id) &
                           (pd.to_datetime(vitals['date']) <= pred_dt)]
    latest_bp_s = recent_vitals.sort_values(by='date', ascending=False).iloc[0]['bp_systolic'] if not recent_vitals.empty else None
    latest_bp_d = recent_vitals.sort_values(by='date', ascending=False).iloc[0]['bp_diastolic'] if not recent_vitals.empty else None

    combined_features = {
        **nlp_features,
        "latest_hba1c": latest_hba1c,
        "latest_cholesterol": latest_cholesterol,
        "latest_bp_systolic": latest_bp_s,
        "latest_bp_diastolic": latest_bp_d,
        # ... other features
    }
    return combined_features

print("\n--- Multi-Modal Features for Patient P001 on 2023-05-20 ---")
patient_p001_features = get_features_for_patient("P001", "2023-05-20")
for feature, value in patient_p001_features.items():
    print(f"{feature}: {value}")
