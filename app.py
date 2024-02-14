import streamlit as st

# Welcome Message
st.markdown("""
# Welcome to JUVA MED
### Advanced Radiology Diagnostic System
We hope our AI doctor can diagnose your ailment and assist you with your medical condition.
""")

if not st.session_state.get('info_status',''):
    st.session_state['info_status'] = False
def main():
    

    # Sidebar with Upload File options
    with st.sidebar:
        st.write("# Upload Files")
        imaging_files = st.file_uploader("Choose Image files to upload", type=["pdf", "jpg", "jpeg", "png"])
        medical_record = st.file_uploader("Choose Medical record to upload", type=["pdf", "jpg", "jpeg", "png"])

    # Form on the main page
    container  = st.empty()
    with container.form("# Patient Information") as cont:
        st.write("# Patient Information")
        age = st.number_input("Age", value=25, step=1)
        marital_status = st.radio("Marital Status", options=["Single", "Married", "Divorced", "Widowed"])
        gender = st.radio("Gender", options=["Male", "Female", "Other"])
        smoke = st.checkbox("Smoke?")
        drink = st.checkbox("Drink?")
        exercises = st.checkbox("Exercises?")
        other_info = st.text_area("Other Information")
        submitted = st.form_submit_button("Submit")
        if submitted:
            with st.spinner("Proccesing Information"):
                st.success("Information has be stored")
            # Process data
            # Placeholder: This is where you would process the form data and uploaded files, e.g., send to backend
            st.write("Processing Data...")
            st.write("Data Received: ")
            st.write(f"Age: {age}, Marital Status: {marital_status}, Gender: {gender}")
            st.write(f"Smoke: {smoke}, Drink: {drink}, Exercises: {exercises}")
            st.write(f"Other Info: {other_info}")
            if imaging_files:
                st.write("Uploaded Files:")
                for file in imaging_files:
                    st.write(file.name)
            
            if medical_record:
                st.write("Uploaded Files:")
                for file in medical_record:
                    st.write(file.name)
            st.session_state['info_status'] = True
            return True
        else:
            return False
    

if st.session_state['info_status']:
    # Chat Interface
    st.write("# Chat Interface")
    user_input = st.chat_input("Ask JUVA MED Something")
    # Placeholder: This is where you would integrate with your AI Doctor model to provide responses
    if user_input:
        ai_response = "JUVA MED is at your service"
        st.write(f"AI Response: {ai_response}")
else:
    main()
