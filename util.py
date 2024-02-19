import streamlit as st
def init_messages() -> None:
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    
    if clear_button or "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", 
                                         "content": "Welcome to JUVA MED!! Start by explaining your ailment?"}]
 