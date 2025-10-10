import os
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_bird_fact(bird_name):
    """
    Calls an AI service to generate a fun fact about the bird.
    Returns a string fact or None
    """

    if not GEMINI_API_KEY:
        logger.error("Gemini API key not found")
        return None
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt_text = f"Tell me a fun fact about the bird species: {bird_name}."

        # Call the AI service (stubbed)
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Fast and efficient for description tasks
            contents=[prompt_text]
        )

        fact = getattr(response, "output_text", None)
        if not fact:
            logger.warning(f"No output text returned for {bird_name}. Full response: {response}")
            return f"This is a {bird_name}. (AI fact unavailable)"

        return fact.strip()
    except Exception as e:
        logger.error(f"Error generating AI fact for {bird_name}: {e}")
        return f"This is a {bird_name}. (AI fact unavailable)"
    
# Example usage:
# fact = generate_bird_fact("northern cardinal")
# print(fact)