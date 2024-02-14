import streamlit as st
import time

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
            st.session_state.imaging_files = st.file_uploader("Choose Image files to upload", type=["jpg", "jpeg", "png"],
                                            )
            st.session_state.medical_record = st.file_uploader("Choose Medical record to upload", type=["pdf"])

        # Form on the main page
        
        with container.form("# Patient Information") as cont:
            st.write("# Patient Information")
            st.session_state.age = st.number_input("Age", value=25, step=1)
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
        st.write(f"Marital Status: {st.session_state.marital_status}")
        st.write(f"Gender: {st.session_state.gender}")
        st.write(f"Smoke: {st.session_state.smoke}")
        st.write(f"Drink: {st.session_state.drink}")
        st.write(f"Exercises: {st.session_state.exercises}")
        st.write(f"Other Info: {st.session_state.other_info}")
        if st.session_state.imaging_files:
            st.write("Uploaded Files:")
            #for file in imaging_files:
                #img = file.read()
            st.image(st.session_state.imaging_files)
        
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
    # Chat Interface
    st.write("# Consultation Session")
    user_input = st.chat_input("Ask JUVA MED Something")
    # Placeholder: This is where you would integrate with your AI Doctor model to provide responses
    if user_input:
        ai_response = "JUVA MED is at your service"
        st.write(f"AI Response: {ai_response}")
else:
    main()
