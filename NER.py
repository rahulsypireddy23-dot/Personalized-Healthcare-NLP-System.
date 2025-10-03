from transformers import pipeline

# For medical NER, you'd ideally use a model fine-tuned on clinical data.
# Example of a general NER model (for illustration, not clinically specific)
# For clinical NER, you would look for models like:
# 'microsoft/BiomedNLP-PubMedBERT-base-uncased' combined with a specific NER head
# or models available on the Hugging Face hub fine-tuned for medical tasks.

# Let's assume you have access to a fine-tuned medical NER model.
# For demonstration, we'll use a generic one and illustrate the concept.
# In a real scenario, you'd use a model like 'samrawal/bert-base-uncased_clinical-ner' or similar.

try:
    # Attempt to load a clinical NER model if available
    ner_pipeline = pipeline("ner", model="samrawal/bert-base-uncased_clinical-ner", aggregation_strategy="simple")
    print("Using 'samrawal/bert-base-uncased_clinical-ner' for NER.")
except Exception:
    print("Clinical NER model not found or failed to load. Falling back to generic NER for demonstration.")
    ner_pipeline = pipeline("ner", aggregation_strategy="simple") # Fallback to a generic NER model

def extract_entities(text):
    entities = ner_pipeline(text)
    structured_entities = []
    for entity in entities:
        structured_entities.append({
            "text": entity['word'],
            "entity_type": entity['entity_group'],
            "score": entity['score'],
            "start": entity['start'],
            "end": entity['end']
        })
    return structured_entities

# Example clinical record snippet
clinical_record = """
Patient presented with severe chest pain radiating to the left arm. Blood pressure was 140/90 mmHg.
ECG showed ST elevation in leads V2-V4. Administered Aspirin 325mg and Nitroglycerin.
Past medical history includes Type 2 Diabetes Mellitus diagnosed 5 years ago, managed with Metformin.
No known drug allergies.
"""

print("--- Extracted Entities ---")
extracted = extract_entities(clinical_record)
for ent in extracted:
    print(f"Entity: {ent['text']}, Type: {ent['entity_type']}")
