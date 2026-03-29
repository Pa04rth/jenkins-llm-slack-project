# File responsible to analyze the last 200 lines of the log file and extract the relevant information for the dashboard.

def parse_log_file(log_file_path):
    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()[-200:]  # Read the last 200 lines of the log file

    parsed_data = []
    for line in lines:
        #the log line format is: "timestamp - level - message"
        parts = line.strip().split(' - ')
        if len(parts) >= 3:
            timestamp, level, message = parts[0], parts[1], ' - '.join(parts[2:]) # Seprate the timestamp, level and rest message from the log line
            parsed_data.append({
                'timestamp': timestamp,
                'level': level,
                'message': message
            })
    return parsed_data 

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

