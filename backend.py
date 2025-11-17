import os
import json
import google.generativeai as genai
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import streamlit as st

 
 
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

quad_url = st.secrets["QDRANT_URL"]
quadrant_api_key= st.secrets["QDRANT_API_KEY"]

gemini_model = genai.GenerativeModel("gemini-2.0-flash")

 

 
qdrant = QdrantClient(
    url= quad_url,
    api_key= quadrant_api_key
)

 
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def detect_emotion(text):
    """Uses Gemini to categorize emotion from user text."""
    prompt = f"""
    You are an emotion detection assistant.
    Analyze the following text and return ONE emotion word (e.g., sad, anxious, angry, calm, stressed, hopeful).
    Text: "{text}"
    """
     
    parts = [{"text": prompt}]
    response = gemini_model.generate_content(parts)
    return response.text.strip().lower()

def retrieve_insights(query, top_k=3):
    """Searches Qdrant for most relevant stress insights."""
    vector = embedder.encode(query).tolist()
    results = qdrant.search(
        collection_name="stress_insights",
        query_vector=vector,
        limit=top_k
    )
    return [hit.payload["text"] for hit in results]

def stress_response(user_text,base64_audio=None):
    
    emotion = detect_emotion(user_text)
    print(f"🧩 Detected emotion: {emotion}")

    
    context_texts = retrieve_insights(user_text)
    context = "\n\n".join(context_texts)
    print(f"🧠 Retrieved {len(context_texts)} insights")
 
    prompt = f"""
    You are a caring mental health assistant.
    The user is feeling {emotion}.
    
    Here are relevant book insights from memory:
    --------------------------------------------
    {context}

    User message: "{user_text}"
    Respond with:
    1. An empathetic acknowledgment that reflects the user’s feelings.
    2. 1–2 short stress-coping tips (scientifically grounded or based on CBT/mindfulness).
    3. 2 practical next steps the user can apply today.
    4. 1 key insight or inspiring quote from the retrieved text above.
    5. Mention the reference book and author when giving the suggestion (e.g., “as Daniel Chidiak explains in *Stop Letting Everything Affect You*”).
        # Respond with:
    # 1. Empathetic acknowledgment.
    # 2. 1–2 short stress coping tips.
    # 3. 2 practical next steps.
    # 4. 1 key insight from the retrieved text above.
    """
    
    parts = [{"text": prompt}]
    if user_text:
        parts.append({"text": user_text})
    if base64_audio:
        parts.append({"inline_data": {"mime_type": "audio/wav", "data": base64_audio}})

     
    response = response = gemini_model.generate_content(parts)
        
   
    return {"analysis": response.text}
