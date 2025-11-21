import os
import json
from datetime import datetime

class Logger:
    def __init__(self, log_dir='logs'):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def log(self, message):
        print(f"[{datetime.now().isoformat()}] {message}")

    def save_session(self, input_text, results, trace):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Save log
        filename = f"run_{timestamp}.log"
        filepath = os.path.join(self.log_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(trace, f, indent=2)
        self.log(f"Session trace saved to {filepath}")
        # Save demo session
        demo_dir = 'demo_loops'
        os.makedirs(demo_dir, exist_ok=True)
        demo_filename = f"session_{timestamp}.json"
        demo_filepath = os.path.join(demo_dir, demo_filename)
        session_data = {"input": input_text, "results": results, "trace": trace}
        with open(demo_filepath, 'w') as f:
            json.dump(session_data, f, indent=2)
        self.log(f"Session saved to {demo_filepath}")