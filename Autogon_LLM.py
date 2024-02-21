import requests
import json

def chat_with_autogon(session_id, question, autogon_api):
    url = "https://api.autogon.ai/api/v1/services/chatbot/e71fcd98-b129-4145-980b-1c14b2f991c5/chat/"

    payload = {
        "session_id": session_id,
        "question": question
    }

    headers = {
        'Content-Type': 'application/json',
        "X-AUG-KEY": autogon_api 
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["data"]["bot_response"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Example usage:
session_id = "36d37fe0-8efd-4deb-9bc7-d873fefdaf52"

question = "list what you know?"


#result = chat_with_autogon(session_id, question, autogon_api_key)
#print("Chatbot response:", result)