import streamlit as st
import requests

def show():
    # Custom CSS for styling
    st.markdown("""
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f0f0f0;
        color: #333;
    }
    .stButton > button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    .stCheckbox {
        margin-bottom: 15px;
    }
    .stSelectbox {
        margin-bottom: 15px;
    }
    .stNumberInput {
        margin-bottom: 20px;
    }
    .stWarning {
        color: #dc3545;
    }
    .stSuccess {
        color: #28a745;
    }
    .stInfo {
        color: #17a2b8;
    }
    .stSubheader {
        font-size: 24px;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .stWrite {
        font-size: 18px;
        margin-bottom: 10px;
    }
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    .activity-container h2 {
        font-size: 22px;
        margin-bottom: 15px;
    }
    .activity-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
</style>
    """, unsafe_allow_html=True)

    # Header section
    st.title("Contact Us")
    st.subheader("SahaYatri - Discover Personalized Travel Experiences Within Your Budget")

    # Introduction text
    st.markdown("""We understand the struggle of finding the perfect places to visit that fit your budget. Whether you're looking for a quick hangout spot with friends or planning a full-blown trip, Sahayatri offers personalized recommendations based on your budget and interests.""")

    # Initialize session state variables
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False

    # Check if the form was just submitted
    if st.session_state.form_submitted:
        st.success("Thank you for your message! We will get back to you soon.")
        # Reset the form_submitted state
        st.session_state.form_submitted = False
    
    # Contact form
    with st.form(key='contact_form'):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        subject = st.text_input("Subject")
        message = st.text_area("Message")

        # Submit button
        submit_button = st.form_submit_button(label='Submit')
        
    if submit_button:
        if not name or not email or not message:
            st.error("Please fill out all fields.")
        else:
            form_data = {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message
            }
            # Submit form data to Formspree endpoint
            response = requests.post('https://formspree.io/f/mpwawqyr', data=form_data)

            if response.status_code == 200:
                st.session_state.form_submitted = True
                # Rerun the app to show the success message and clear the form
                st.experimental_rerun()
            else:
                st.error("Oops! Something went wrong. Please try again later.")
st.write("\n")

if __name__ == '__main__':
    show()
