# File responsible to analyze the last 200 lines of the log file and extract the relevant information for the dashboard.
import os
def parse_log_file(file_path):
    """
    Reads the Jenkins log file and returns it as a clean text string.
    """
    if not os.path.exists(file_path):
        return "ERROR: Log file not found at " + file_path

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the whole file into a single string
            log_content = file.read().strip()
            
            if not log_content:
                return "ERROR: Log file was empty."
                
            return log_content
            
    except Exception as e:
        return f"ERROR: Could not read log file. Details: {e}"

# parsed data example -[
#     {
#         'timestamp': '2026-03-26 10:00:00',
#         'level': 'INFO',
#         'message': 'Server started'
#     },
#     {
#         'timestamp': '2026-03-26 10:01:00',
#         'level': 'ERROR',
#         'message': 'Database connection failed'
#     }
# ]

