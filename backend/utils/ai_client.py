import os
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_bird_fact(bird_name):
    """
    Calls an AI service to generate a fun fact about the bird.
    Returns a string fact or a fallback.
    """
    if not GEMINI_API_KEY:
        logger.error("Gemini API key not found")
        return None

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt_text = f"Tell me a fun fact about the bird species: {bird_name}."

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt_text]
        )

        # Grab the actual text from candidates
        fact = None
        if hasattr(response, "candidates") and response.candidates:
            fact_parts = response.candidates[0].content.parts
            if fact_parts:
                fact = fact_parts[0].text.strip()

        if not fact:
            logger.warning(f"No output text returned for {bird_name}. Full response: {response}")
            fact = f"This is a {bird_name}. (AI fact unavailable)"

        return fact

    except Exception as e:
        logger.error(f"Error generating AI fact for {bird_name}: {e}")
        return f"This is a {bird_name}. (AI fact unavailable)"
