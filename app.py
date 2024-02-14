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

def main():
    

    # Sidebar with Upload File options
    with st.sidebar:
        st.write("# Upload Files")
        imaging_files = st.file_uploader("Choose Image files to upload", type=["jpg", "jpeg", "png"],
                                         )
        medical_record = st.file_uploader("Choose Medical record to upload", type=["pdf"])

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
        st.session_state['info_status'] = True
        container.empty()
        # Process data
        # Placeholder: This is where you would process the form data and uploaded files, e.g., send to backend
        st.write("Processing Data...")
        st.write("Data Received: ")
        st.write(f"Age: {age}, Marital Status: {marital_status}, Gender: {gender}")
        st.write(f"Smoke: {smoke}, Drink: {drink}, Exercises: {exercises}")
        st.write(f"Other Info: {other_info}")
        if imaging_files:
            st.write("Uploaded Files:")
            #for file in imaging_files:
                #img = file.read()
            st.image(imaging_files)
        
        if medical_record:
            st.write("Uploaded Files:")
            #for file in medical_record:
            st.write(medical_record.name)
    st.markdown("#### Please confirm the above Information!!")
    if st.button("Confirm"):
        st.session_state['info_status'] = True
            
            

print(st.session_state['info_status'])
if st.session_state['info_status']:
    st.success("Information has be stored")
    with st.spinner("We are setting your schedule with AI Doctor"):
        time.sleep(3)
    # Chat Interface
    st.write("# Consultation Session")
    user_input = st.chat_input("Ask JUVA MED Something")
    # Placeholder: This is where you would integrate with your AI Doctor model to provide responses
    if user_input:
        ai_response = "JUVA MED is at your service"
        st.write(f"AI Response: {ai_response}")
else:
    main()
