import requests
import os
import json
from dotenv import load_dotenv
load_dotenv() 
def send_slack_alert(ai_summary, build_url="Local Test"):
    """
    Sends the AI-generated build summary to a Slack channel.
    """
    # Pull the webhook URL from environment variables
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    
    if not webhook_url:
        print("SLACK_WEBHOOK_URL not found. Skipping Slack notification.")
        return

    # Slack uses a specific JSON structure. We'll use basic Markdown for styling.
    message_payload = {
        "text": f"*Jenkins Build Failure Detected* \n\n*Build URL:* {build_url}\n\n*AI Root Cause Analysis & Fix:*\n> {ai_summary}"
    }

    try:
        response = requests.post(
            webhook_url, 
            data=json.dumps(message_payload),
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status() # Throws an error if the request fails
        print("Successfully pushed AI analysis to Slack!")
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Slack alert: {e}")