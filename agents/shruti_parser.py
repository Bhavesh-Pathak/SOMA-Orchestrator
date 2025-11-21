import requests

class ShrutiParserAgent:
    def __init__(self, url='http://localhost:8000/analyze'):
        self.url = url

    def run(self, text: str) -> dict:
        try:
            response = requests.post(self.url, json={"text": text}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to call Shruti Parser: {e}")