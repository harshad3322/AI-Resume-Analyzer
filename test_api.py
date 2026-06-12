import os
import requests
from dotenv import load_dotenv

load_dotenv()

response = requests.post(
    "https://app.backboard.io/api/threads/messages",
    headers={
        "X-API-Key": os.getenv("BACKBOARD_API_KEY"),
        "Content-Type": "application/json"
    },
    json={
        "content": "Reply with hello"
    }
)

print("Status Code:", response.status_code)
print(response.text)