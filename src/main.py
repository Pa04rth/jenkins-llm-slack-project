import sys
import os
# Assume you have your other modules built
from log_parser import parse_log_file as extract_logs
from llm_client import call_llm_api as get_ai_summary
from slack_notifier import send_slack_alert

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <path_to_log_file>")
        sys.exit(1)

    log_path = sys.argv[1]
    
    # 1. Parse the log
    print(f"Parsing log file: {log_path}...")
    log_text = extract_logs(log_path)
    
    # 2. Get the AI Summary
    print("Analyzing with LLM...")
    ai_summary = get_ai_summary(log_text)
    
    # 3. Print to Jenkins Console (This happens automatically via standard output)
    print("\n" + "="*40)
    print("AI DevOps Assistant Summary:")
    print("="*40)
    print(ai_summary)
    print("="*40 + "\n")
    
    # 4. Send to Slack
    # We grab the BUILD_URL injected automatically by Jenkins
    jenkins_build_url = os.getenv("BUILD_URL", "Run Locally")
    send_slack_alert(ai_summary, jenkins_build_url)

if __name__ == "__main__":
    main()