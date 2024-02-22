import streamlit as st
import time
import os
from dotenv import load_dotenv
from util import init_messages, load_image, update_image_analysis
from Autogon_LLM import chat_with_autogon, session_id
from Image_dt import generate_medical_description
from langchain.agents.react.agent import create_react_agent
from langchain.agents import AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI


from util import tools, prompt, base_template



load_dotenv()

user_prompt = "Please describe the symptoms or relevant details about the medical image."

#autogon_api_key = "5yDUI8MA.9Sg5UHCNTXlmupUFxX6xSPzymo837tXG" #os.environ['AUTOGON_API_KEY']

st.set_page_config(
    )
# Welcome Message
st.markdown("""
# Welcome to JUVA MED
### Advanced Radiology Diagnostic System
We hope our AI doctor can diagnose your ailment and assist you with your medical condition.
""")

if not st.session_state.get('info_status',''):
    st.session_state['info_status'] = False
    

def onclick():
    st.success("Information has be stored")
    with st.spinner("We are setting your schedule with AI Doctor"):
        time.sleep(3)
    st.session_state['info_status'] = True

def main():
    
    container  = st.empty()
    if not st.session_state.get('submitted', ''):
        # Sidebar with Upload File options
        with st.sidebar:
            st.write("# Upload Files")
            st.session_state.imaging_file = st.file_uploader("Choose Image files to upload", type=["jpg", "jpeg", "png"],
                                            )
            st.session_state.medical_record = st.file_uploader("Choose Medical record to upload", type=["pdf"])

        # Form on the main page
        
        with container.form("# Patient Information") as cont:
            st.write("# Patient Information")
            st.session_state.age = st.number_input("Age", value=25, step=1)
            st.session_state.weight = st.number_input("Weight")
            st.session_state.height = st.number_input("Height")
            st.session_state.marital_status = st.radio("Marital Status", options=["Single", "Married", "Divorced", "Widowed"])
            st.session_state.gender = st.radio("Gender", options=["Male", "Female", "Other"])
            st.session_state.smoke = st.checkbox("Smoke?")
            st.session_state.drink = st.checkbox("Drink?")
            st.session_state.exercises = st.checkbox("Exercises?")
            st.session_state.other_info = st.text_area("Other Information")
            submitted = st.form_submit_button("Submit")
            st.session_state['submitted'] = submitted

    if st.session_state['submitted']:
        st.session_state['submitted'] = True
        container.empty()
        # Process data
        st.session_state['info_status'] = True
        # Placeholder: This is where you would process the form data and uploaded files, e.g., send to backend
        st.write("Data Received: ")
        st.write(f"Age: {st.session_state.age}")
        st.write(f"Weight: {st.session_state.weight}")
        st.write(f"Weight: {st.session_state.height}")
        st.write(f"Marital Status: {st.session_state.marital_status}")
        st.write(f"Gender: {st.session_state.gender}")
        st.write(f"Smoke: {st.session_state.smoke}")
        st.write(f"Drink: {st.session_state.drink}")
        st.write(f"Exercises: {st.session_state.exercises}")
        st.write(f"Other Info: {st.session_state.other_info}")
        if st.session_state.imaging_file:
            st.write("Uploaded Images:")
            #for file in imaging_files:
                #img = file.read()
            st.image(st.session_state.imaging_file)
        
        if st.session_state.medical_record:
            st.write("Uploaded Files:")
            #for file in medical_record:
            st.write(st.session_state.medical_record.name)

            st.markdown("#### Please confirm the above Information!!")

        if not st.button("Confirm", on_click=onclick):
            st.session_state['info_status'] = False
            pass
                
            

print(st.session_state['info_status'])
if st.session_state['info_status']:
    google_api_key = st.secrets['GOOGLE_API_KEY']
    #google_api_key = os.environ['GOOGLE_API_KEY']
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)
    #result = llm.invoke("Write a ballad about LangChain")
    #print(result.content)
    # Construct the ReAct agent
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    # Chat Interface
    if (not st.session_state.image_analysis) and (st.session_state.imaging_file):
        image_url = load_image(st.session_state.imaging_file)
        result = generate_medical_description(user_prompt, image_url)
        #st.write("Image Description: "+ result.content)
        update_image_analysis(result.content)
        #st.session_state['image_analysis'] = result.content
        st.session_state.base_prompt = """Below is the analysis of the user's medical scan. Kindly give a medical advice based on this. \nNote: Your new task is to assume a medical role\n\n
                            Medical Scan Description: {}

                            Question: {}

                            Try as much as you can to provide relevant answer and help this patient. 
                            """
    else:
        st.session_state.base_prompt = ''
    
    st.write("# Consultation Session")
    init_messages()
    messages = []
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
        messages.append(f"{msg['role']}: {msg['content']}")

    if st.session_state.get('get_new_img'):
        st.session_state.new_file = st.sidebar.file_uploader("Choose Image files to upload", type=["jpg", "jpeg", "png"] )
        if st.session_state.new_file:
            img =  load_image(st.session_state.new_file)
            with st.spinner("JuvaMed is Analysing Image"):
                res  = generate_medical_description(user_prompt, img)
                st.session_state.new_img_desc = res.content
                update_image_analysis(st.session_state.new_img_desc)
                st.session_state['get_new_img'] = False
        else:
            st.stop()
    user_input = st.chat_input("Consult JUVA MED")
    # Placeholder: This is where you would integrate with your AI Doctor model to provide responses
    if user_input:
        #final_input = st.session_state.base_prompt.format(st.session_state.image_analysis,user_input)
        st.chat_message("user").write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        #response = chat_with_autogon(session_id, final_input, autogon_api_key)
        try:
            with st.spinner("JuvaMed is Reasoning"):
                response = agent_executor.invoke({'input':user_input, 'chat_history':messages})
                #ai_response = "JUVA MED is at your service"
            st.chat_message("assistant").write(response['output'])
            st.session_state.messages.append({"role": "assistant", "content": response['output']})
        except Exception as err:
            st.error("Oops! Error Occured, when generating response!!")

else:
    main()
