import os
import requests
import dotenv
dotenv.load_dotenv()


def get_ai_summary(log_text):
    """
    Sends the prompt and the parsed log to the Gemini API and returns the summary.
    """
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        return "⚠️ Error: LLM_API_KEY environment variable not found."

    # The API endpoint for Gemini 2.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    # BUG FIX 1: We inject the actual log_text into the prompt string using f-strings
    full_prompt = f"""
    You are an expert DevOps engineer. Analyze the following Jenkins build log snippet. 
    Identify the root cause of the failure, explain it in one sentence, and provide a 2-step actionable fix.
    
    === BEGIN JENKINS LOG ===
    {log_text}
    === END JENKINS LOG ===
    """

    payload = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }]
    }

    try:
        # Send the request to Google
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        response.raise_for_status() # Throw an error if the request fails
        
        data = response.json()
        
        # BUG FIX 2: Dig into the JSON dictionary to extract ONLY the AI's text response
        clean_ai_text = data['candidates'][0]['content']['parts'][0]['text']
        
        return clean_ai_text
        
    except Exception as e:
        return f"❌ AI Analysis Failed: {e}"