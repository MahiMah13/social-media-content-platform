import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_social_post(company_name: str, topic: str, platform: str, brand_voice: str = "professional"):
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    You are an expert social media manager.
    Create a post for the company '{company_name}'.
    
    - Target Platform: {platform}
    - Topic/Goal: {topic}
    - Brand Voice/Tone: {brand_voice}
    
    Provide output in the following JSON format:
    {{
        "caption": "The main post caption text here",
        "hashtags": ["#tag1", "#tag2", "#tag3"],
        "call_to_action": "The suggested call to action"
    }}
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    return response.text
