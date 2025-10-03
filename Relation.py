# --- Relation Extraction (Conceptual) ---
# This part is more complex and usually involves:
# 1. Identifying pairs of entities.
# 2. Feeding the sentence with entity markers to a relation extraction model.
# 3. The model predicts the relationship type (e.g., 'treats', 'causes', 'diagnosed_with').

# For demonstration, let's create a very basic, rule-based relation extraction
# This is NOT robust for a real system, but illustrates the idea.
# In a real project, you'd use a fine-tuned RE model (e.g., using a Hugging Face model
# trained on a medical relation extraction dataset like ChemProt, GAD, etc.).

def extract_relations_rule_based(text, entities):
    relations = []
    # Example: Link drugs to diseases if they appear in proximity or with keywords
    drugs = [e for e in entities if 'DRUG' in e['entity_type'].upper()] # Using 'DRUG' from clinical-ner output
    diseases = [e for e in entities if 'PROBLEM' in e['entity_type'].upper() or 'DISEASE' in e['entity_type'].upper()]

    # Very simple proximity-based linking
    for drug in drugs:
        for disease in diseases:
            # Check if drug and disease are in the same sentence and reasonably close
            if abs(drug['start'] - disease['start']) < 100 and \
               (drug['text'] in text and disease['text'] in text): # Basic check
                # A real RE model would classify the *type* of relation
                relations.append({
                    "entity1": drug['text'],
                    "entity1_type": drug['entity_type'],
                    "relation_type": "TREATS/MANAGES", # Placeholder
                    "entity2": disease['text'],
                    "entity2_type": disease['entity_type']
                })
    return relations

print("\n--- Extracted Relations (Rule-Based, for illustration) ---")
# Adjusting entity types based on the 'clinical-ner' model's output
# Common entity types for clinical-ner might be 'Problem', 'Test', 'Treatment'
clinical_record_entities = [
    {'text': 'chest pain', 'entity_type': 'Problem', 'start': 24, 'end': 34},
    {'text': 'Type 2 Diabetes Mellitus', 'entity_type': 'Problem', 'start': 177, 'end': 201},
    {'text': 'Aspirin', 'entity_type': 'Treatment', 'start': 118, 'end': 125},
    {'text': 'Nitroglycerin', 'entity_type': 'Treatment', 'start': 136, 'end': 149},
    {'text': 'Metformin', 'entity_type': 'Treatment', 'start': 222, 'end': 231}
]

# Update relation extraction to use 'Treatment' and 'Problem'
def extract_relations_enhanced(text, entities):
    relations = []
    treatments = [e for e in entities if e['entity_type'] == 'Treatment']
    problems = [e for e in entities if e['entity_type'] == 'Problem']

    for treatment in treatments:
        for problem in problems:
            # More sophisticated logic needed here, e.g., dependency parsing, sentence-level analysis
            # For this simple example, we'll just link if they appear in the same general context
            # and the treatment could plausibly address the problem.
            if f"administered {treatment['text']}" in text.lower() and problem['text'] in text.lower() and \
               treatment['start'] < problem['start']: # Very basic ordering assumption
                if "chest pain" in problem['text'].lower() and ("aspirin" in treatment['text'].lower() or "nitroglycerin" in treatment['text'].lower()):
                    relations.append({
                        "entity1": treatment['text'],
                        "entity1_type": treatment['entity_type'],
                        "relation_type": "TREATS",
                        "entity2": problem['text'],
                        "entity2_type": problem['entity_type']
                    })
                elif "diabetes" in problem['text'].lower() and "metformin" in treatment['text'].lower():
                     relations.append({
                        "entity1": treatment['text'],
                        "entity1_type": treatment['entity_type'],
                        "relation_type": "MANAGES",
                        "entity2": problem['text'],
                        "entity2_type": problem['entity_type']
                    })
    return relations

relations = extract_relations_enhanced(clinical_record.lower(), extracted)
for rel in relations:
    print(f"{rel['entity1']} ({rel['entity1_type']}) --[{rel['relation_type']}]--> {rel['entity2']} ({rel['entity2_type']})")
