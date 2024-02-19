import os
from dotenv import load_dotenv
from Autogon_LLM import chat_with_autogon, session_id
from Image_dt import generate_medical_description
load_dotenv()

autogon_api_key = os.environ['AUTOGON_API_KEY_2']

question = "Are you willing to learn about medical diagnoses"

result = chat_with_autogon(session_id, question, autogon_api_key)

print("Chatbot response:", result)



user_prompt = "Please describe the symptoms or relevant details about the medical image."
image_url = r'./images/Normal-CT-head-5Age-30-40.jpg'
result = generate_medical_description(user_prompt, image_url)
print("Image Description", result)