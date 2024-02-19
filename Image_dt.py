from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import time
import os
from dotenv import load_dotenv
load_dotenv()

def generate_medical_description(user_prompt, image_url):
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
    llm = ChatGoogleGenerativeAI(model="gemini-pro-vision", google_api_key=GOOGLE_API_KEY)

    # Base prompt for the model to take the role of a doctor describing a medical image
    base_prompt = "As a medical professional, analyze and describe the clinical findings present in the provided image. Include details such as relevant symptoms, potential diagnoses, and any notable observations. Your detailed description will assist in understanding the medical context of the image."


    modified_user_prompt = f"{base_prompt}\n\n{user_prompt}\n\nPlease ensure that your response focuses on medical details."

    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            message = HumanMessage(
                content=[
                    {"type": "text", "text": modified_user_prompt},
                    {"type": "image_url", "image_url": image_url},
                ]
            )

            # Invoke the model with the user's message
            response = llm.invoke([message])

            # Return or handle the model's response
            return response

        except Exception as e:
            print(f"Error: {e}")
            retries += 1
            print(f"Retrying in 5 seconds (Attempt {retries}/{max_retries})")
            time.sleep(5)

    print("Maximum retries reached. Unable to get a response.")
    return None  



user_prompt = "Please describe the symptoms or relevant details about the medical image."
image_url = r'C:\Users\Whaleeu\Downloads\images (1).jpeg'
result = generate_medical_description(user_prompt, image_url)
result