from transformers import pipeline

# Load a summarization pipeline
summarizer = pipeline("summarization", model="t5-small")

def summarize_conversation(conversation_text, max_length=150, min_length=30):
    summary = summarizer(conversation_text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

# Example Doctor-Patient Conversation
conversation = """
Doctor: Good morning, Mrs. Smith. What brings you in today?
Patient: Good morning, doctor. I've been feeling very tired lately, and I've had a persistent cough for about three weeks now.
Doctor: I see. Is the cough dry or productive? Any fever or shortness of breath?
Patient: It's mostly dry, sometimes I bring up a little phlegm. No fever, but I do feel a bit breathless after climbing stairs.
Doctor: Alright. Let's listen to your lungs. (listens) I hear some crackles in your lower left lobe. Have you had any recent travel or exposure to sick individuals?
Patient: No recent travel. My grandson had a cold last month, but he's fine now.
Doctor: Okay. Based on your symptoms and what I'm hearing, it sounds like you might have a mild pneumonia. We'll need to do a chest X-ray to confirm. I'd like to prescribe you Amoxicillin 500mg, three times a day for 7 days. Also, try to get plenty of rest and stay hydrated. We'll schedule a follow-up in one week.
Patient: Pneumonia? Oh dear. Will I be able to go to work?
Doctor: I'd recommend taking a few days off to rest. The Amoxicillin should start working within 48 hours. If your symptoms worsen or you develop a high fever, please come back sooner or go to the emergency room.
Patient: Okay, thank you, doctor.
Doctor: You're welcome. We'll send the X-ray request and prescription to your pharmacy.
"""

print("\n--- Conversation Summary ---")
summary = summarize_conversation(conversation)
print(summary)
