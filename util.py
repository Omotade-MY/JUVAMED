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

When providing a diagnosis and medical advice, keep to these template:

1. Think about the symptoms and what information you need.
2. If there is need for additional information then you should ask the user. 
2. Provide a probabilistic response, indicating the likelihood of the medical condition.
3. Offer specific medical advice, outlining recommended next steps for the user/patient to follow.
4. Give a concluisve diagnoses and recommend possible treatment.

To ensure an accurate and safe diagnosis, you may request additional information from the user.\n
You should only use a tool if it is needed""" + base_template

def init_messages(add_msg='') -> None:
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    
    if clear_button or "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", 
                                         "content": "Welcome to JUVA MED!! Start by explaining your ailment?"}]
 
@st.cache_data
def load_image(uploaded_file):
    image_data = uploaded_file.read()
    img = Image.open(BytesIO(image_data))
    return img

def get_ct_scan(inp=None):
    
    #user_prompt = "Please describe the symptoms or relevant details about the medical image."
    #image_url = r'./images/Normal-CT-head-5Age-30-40.jpg'
    #result = generate_medical_description(user_prompt, image_url)
    #print("Image Description", result.content)
    content = """Image Description  The image is a CT scan of the head. It shows a large area of low density in the right frontal lobe of the brain. This is likely caused by a contusion, which is a bruise of the brain tissue. The contusion is probably the result of a traumatic brain injury, such as a car accident or a fall.

            The patient may have a headache, nausea, vomiting, and confusion. They may also have difficulty speaking or moving their right arm or leg.

            The treatment for a contusion is typically supportive. The patient may be given pain medication and anti-inflammatory drugs. They may also need to have surgery to remove the contusion if it is causing significant problems.

            The prognosis for a contusion depends on the size and location of the injury. Most contusions heal completely, but some patients may have permanent problems, such as memory loss or difficulty speaking."""
    return content

def get_xray_scan(inp=None):
    
    #user_prompt = "Please describe the symptoms or relevant details about the medical image."
    #image_url = r'./images/Normal-CT-head-5Age-30-40.jpg'
    #result = generate_medical_description(user_prompt, image_url)
    #print("Image Description", result.content)
    content = """Image Description  The provided image is an X-ray of a hand. The bones are in the correct alignment, and there are no signs of fracture or dislocation. However, the soft tissues around the bones appear swollen. This could be due to a number of things, including inflammation, infection, or trauma.

            The patient may be experiencing pain, swelling, and stiffness in the hand. They may also have difficulty moving the fingers. If the swelling is severe, it could compress the nerves and blood vessels in the hand, leading to further problems.

            The differential diagnosis for this condition includes a number of things, including:

            * Arthritis
            * Gout
            * Infection
            * Trauma
            * Tumor

            The patient should be evaluated by a doctor to determine the cause of the swelling and to receive appropriate treatment."""
    return "No Xray Image"#content

def ask_user(query):
    #res = input(f"{query}: ")
    st.chat_message('assistant').write(query)
    st.stop()
    return #res

def user_biodata(input=None):
    biodata = f"""t.write("Patient Bio Data")
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
                                get_ct_scan,
                                name= 'ct_image_description',
                                description = "Useful for extracting the user medical CT scan"
                ),
    Tool.from_function(         
                                get_xray_scan,
                                name= 'xray_image_description',
                                description = "Useful for extracting the user medical xray scan."
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