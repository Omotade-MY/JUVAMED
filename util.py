import streamlit as st
from io import BytesIO
from PIL import Image

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