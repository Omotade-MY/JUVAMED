import streamlit as st
from io import BytesIO
from PIL import Image
from langchain.agents.react.agent import create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage
from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.agents import tools, Tool, tool


prompt = hub.pull("hwchase17/react")
base_template = prompt.template

prompt.template = """"I'm JUVAMED, an AI expert in radiology and general medicine. I specialize in analyzing medical images and other relevant information to diagnose medical conditions and provide advice.

Your Task is to provide a diagnose and help a patient better understand their condition

When responding to patients, prioritize:

- First you should analyse the medical image they provide.
- Clarification & Information Gathering: Ask open-ended questions to understand symptoms and medical history.
- check medical images an scan
- Probabilistic Diagnosis: Offer potential diagnoses with likelihood percentages.
- Actionable Next Steps: Recommend specific actions, tests, or consultations based on risk.

Avoid:
- Closed-ended yes/no questions.
- Overly technical language.
- Promoting specific medications.
- Making definitive diagnoses without appropriate information.

Additional Notes:

- Utilize tools only when necessary and relevant to patient safety.
- Maintain a patient-centric approach, avoiding excessive questioning.
- Remember, doctor consultation systems are not replacements for professional medical advice.

**Remember your task is to provide a diagnose""" + base_template

def init_messages(add_msg='') -> None:
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    
    if clear_button or "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", 
                                         "content": "Welcome to JUVA MED!! Start by explaining your ailment?"}]
        #if st.session_state.get('image_analysis'):
        #    st.session_state.messages.append({"role": "assistant", "content": 'You have provided a medical scan\n'+st.session_state['image_analysis']})
       
 
@st.cache_data
def load_image(uploaded_file):
    image_data = uploaded_file.read()
    img = Image.open(BytesIO(image_data))
    return img

def get_medical_scans(inp=None):
    
    
    content = st.session_state['image_analysis']
    
    return content

def get_new_medical_image(query):

    
    if st.session_state.get('new_img_desc'):
        return st.session_state.new_img_desc
    else:
        st.chat_message('assistant').write(query+"\n\nUpload you medical image on the left sidebar") 
        st.session_state.messages.append({"role": "assistant", "content": query}) 
        st.session_state['get_new_img'] = True
        st.rerun()
        
def ask_user(query):
    #res = input(f"{query}: ")
    st.chat_message('assistant').write(query)
    st.session_state.messages.append({"role": "assistant", "content": query})

    st.stop()
    return #res

def respond_to_user(query):
    #res = input(f"{query}: ")
    st.chat_message('assistant').write(query)
    st.session_state.messages.append({"role": "assistant", "content": query})

    st.stop()
    return #res
def user_biodata(input=None):
    biodata = f"""# Patient Bio Data")
        Age: {st.session_state.age}\n
        Weight: {st.session_state.weight}\n
        Height: {st.session_state.height}\n
        Marital Status: {st.session_state.marital_status}\n
        Gender: {st.session_state.gender}\n
        Smoke: {st.session_state.smoke}\n
        Drink: {st.session_state.drink}\n
        Exercises: {st.session_state.exercises}\n
        Other Info: {st.session_state.other_info}"""
    
    return biodata


tools = [
    Tool.from_function(         
                                get_medical_scans,
                                name= 'medical_all_user_image_descriptions',
                                description = "Use this to access all the medical images the user has provided. You should use this tool before asking the user for a medical image"
                ),
    Tool.from_function(         
                                get_new_medical_image,
                                name= 'collect_new_medical_image',
                                description = "Use this to request for new medical image from the user. Use this tool to access new uploaded medical image by the user."
                ),
    
    Tool.from_function(         
                                ask_user,
                                name= 'ask_user',
                                description = "Use this function for asking the user question"
                ),
    Tool.from_function(         
                                user_biodata,
                                name= 'get_biodata',
                                description = "Use this function get some basic prefilled bio information of the user. Use this tool before asking the user questions"
                ),
    
]

def update_image_analysis(img_desc):
    no = len(st.session_state['image_analysis'])
    st.session_state['image_analysis'].update({f'image_description{no+1}': img_desc})

def update_images(img):
    st.session_state['images'].append(img)