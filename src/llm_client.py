# File responsible to have the prompt for the LLM and the function to call the LLM API to get the response.
import requests , os , json
from log_parser import parse_log_file
llm_prompt = """You are an expert DevOps engineer. Analyze the following Jenkins build log snippet. Identify the root cause of the failure, explain it in one sentence, and provide a 2-step actionable fix."""
from dotenv import load_dotenv
load_dotenv()

# Better control using requests.
def call_llm_api(parsed_data):
    
    log_snippet =  "\n".join([
        f"{entry['timestamp']} - {entry['level']} - {entry['message']}"
        for entry in parsed_data
    ])
    
    full_prompt = f"{llm_prompt}\n\nLog Snippet:\n{log_snippet}"
    
    api_key = os.getenv("LLM_API_KEY")
    
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": full_prompt}
                ]
            }
        ]
    }

    response = requests.post(
        f"{url}?key={api_key}",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(f"API Error: {response.text}")

    return response.json()

# example response.json - {
#   "candidates": [
#     {
#       "content": {
#         "parts": [
#           {
#             "text": "LLM response here"
#           }
#         ]
#       }
#     }
#   ]
# }