# --- Knowledge Graphs: Entity Linking (Conceptual) ---

# In a real scenario, you'd use APIs or local databases of terminologies
# (e.g., RxNorm API, SNOMED CT browser, custom ICD-10 lookup).

medical_ontologies = {
    "RxNorm": {
        "Aspirin": "RxCUI: 1191",
        "Nitroglycerin": "RxCUI: 7523",
        "Amoxicillin": "RxCUI: 706",
        "Metformin": "RxCUI: 6809"
    },
    "SNOMED CT": {
        "chest pain": "SNOMED_CT: 29857009",
        "pneumonia": "SNOMED_CT: 6636001",
        "Type 2 Diabetes Mellitus": "SNOMED_CT: 44054006",
        "ST elevation": "SNOMED_CT: 251146004"
    },
    "ICD-10": {
        "Type 2 Diabetes Mellitus": "ICD-10: E11",
        "pneumonia": "ICD-10: J18.9"
    }
}

def link_to_ontology(entity_text, entity_type):
    linked_codes = {}
    normalized_text = entity_text.lower()

    if entity_type == 'Treatment': # Assuming treatments are drugs for simplicity
        for drug_name, rxcui in medical_ontologies["RxNorm"].items():
            if normalized_text in drug_name.lower() or drug_name.lower() in normalized_text:
                linked_codes["RxNorm"] = rxcui
                break
    elif entity_type == 'Problem':
        for snomed_term, snomed_code in medical_ontologies["SNOMED CT"].items():
            if normalized_text in snomed_term.lower() or snomed_term.lower() in normalized_text:
                linked_codes["SNOMED CT"] = snomed_code
                break
        for icd_term, icd_code in medical_ontologies["ICD-10"].items():
            if normalized_text in icd_term.lower() or icd_term.lower() in normalized_text:
                linked_codes["ICD-10"] = icd_code
                break
    # Add logic for other entity types (e.g., 'Test' -> LOINC)

    return linked_codes

print("\n--- Entity Linking to Ontologies (Conceptual) ---")
# Using the entities extracted earlier from clinical_record
for ent in extracted:
    linked = link_to_ontology(ent['text'], ent['entity_type'])
    if linked:
        print(f"Entity: {ent['text']} ({ent['entity_type']}) -> Linked Codes: {linked}")
    else:
        print(f"Entity: {ent['text']} ({ent['entity_type']}) -> No direct link found in conceptual ontologies.")
