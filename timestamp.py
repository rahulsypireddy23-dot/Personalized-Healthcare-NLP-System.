import pandas as pd
from datetime import datetime

# --- Temporal Modeling (Conceptual) ---

patient_records_over_time = [
    {
        "date": "2020-01-15",
        "note": "Patient complains of fatigue. Labs ordered.",
        "entities": [
            {'text': 'fatigue', 'entity_type': 'Problem'}
        ]
    },
    {
        "date": "2020-02-01",
        "note": "Lab results show elevated HbA1c. Diagnosed with Type 2 Diabetes Mellitus. Started Metformin 500mg.",
        "entities": [
            {'text': 'elevated HbA1c', 'entity_type': 'TestResult'},
            {'text': 'Type 2 Diabetes Mellitus', 'entity_type': 'Problem'},
            {'text': 'Metformin', 'entity_type': 'Treatment'}
        ]
    },
    {
        "date": "2021-03-10",
        "note": "Patient presents with chest pain, mild. Advised rest.",
        "entities": [
            {'text': 'chest pain', 'entity_type': 'Problem'}
        ]
    },
    {
        "date": "2023-05-20",
        "note": "Follow-up for diabetes. HbA1c stable. Continue Metformin. Advised cardiac check-up due to recent chest pain episode.",
        "entities": [
            {'text': 'diabetes', 'entity_type': 'Problem'},
            {'text': 'HbA1c stable', 'entity_type': 'TestResult'},
            {'text': 'Metformin', 'entity_type': 'Treatment'},
            {'text': 'cardiac check-up', 'entity_type': 'Test'},
            {'text': 'chest pain episode', 'entity_type': 'Problem'}
        ]
    }
]

def create_patient_timeline(records):
    timeline = []
    for record in sorted(records, key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d")):
        record_date = datetime.strptime(record['date'], "%Y-%m-%d")
        for entity in record['entities']:
            timeline.append({
                "date": record_date,
                "entity_text": entity['text'],
                "entity_type": entity['entity_type']
            })
    return pd.DataFrame(timeline).sort_values(by='date').reset_index(drop=True)

patient_df = create_patient_timeline(patient_records_over_time)
print("\n--- Patient Timeline ---")
print(patient_df)

# Example of a temporal feature: Time since diagnosis
def calculate_time_since_diagnosis(timeline_df, diagnosis_keyword="Diabetes"):
    diagnosis_dates = timeline_df[(timeline_df['entity_type'] == 'Problem') &
                                 (timeline_df['entity_text'].str.contains(diagnosis_keyword, case=False))]['date']
    if not diagnosis_dates.empty:
        first_diagnosis_date = diagnosis_dates.min()
        current_date = datetime.now() # Or a specific prediction date
        time_diff = (current_date - first_diagnosis_date).days / 365.25 # In years
        return round(time_diff, 2)
    return None

time_since_diabetes = calculate_time_since_diagnosis(patient_df, "Diabetes")
print(f"\nTime since Diabetes diagnosis (approx): {time_since_diabetes} years")
