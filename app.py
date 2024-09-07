import streamlit as st
import sqlite3
import hashlib
st.set_page_config(page_title="SahaYatri", page_icon="🌍")
# Import your other pages
import location
import omg
import contact
from PIL import Image
import base64
import requests

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
            .footer {
        padding: 20px;
        text-align: center;
    }
    .footer img {
        width: 70px;
        display: block;
        margin: 0 auto 10px;
    }
    .footer .footer-content {
        max-width: 800px;
        margin: 0 auto;
    }
    .footer .footer-left {
        margin: 10px 0;
    }
    .footer .footer-left h3 {
        font-size: 1.5rem;
        margin: 10px 0;
    }
    .footer .footer-left p {
        font-size: 1rem;
        margin: 10px 0;
    }
    .footer .footer-bottom {
        margin-top: 20px;
        font-size: 0.9rem;
        text-align: center;
    }
    .footer .horizontal-line {
        border: 0.5px solid white;
        margin: 20px 0;
    }
    @media (max-width: 768px) {
        .footer .footer-left h3 {
            font-size: 1.2rem;
        }
        .footer .footer-left p {
            font-size: 0.9rem;
        }
        .footer .footer-bottom {
            font-size: 0.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# JavaScript to scroll to top
st.markdown("""
    <script>
    function scrollToTop() {
        window.scrollTo(0, 0);
    }
    </script>
""", unsafe_allow_html=True)

# Database functions
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('users.db')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result is not None

# Initialize the database
init_db()

# Streamlit app
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.sidebar_state = 'collapsed'

if not st.session_state.authenticated:
    st.title("Login / Sign Up")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.current_page = "Home"
                st.session_state.sidebar_state = 'collapsed'
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
    
    with tab2:
        new_username = st.text_input("New Username", key="signup_username")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        if st.button("Sign Up"):
            if new_username and new_password and new_password == confirm_password:
                if create_user(new_username, new_password):
                    st.success("Account created successfully! You can now log in.")
                else:
                    st.error("Username already exists. Please choose a different username.")
            else:
                st.error("Please fill all fields and ensure passwords match.")

else:
    # Create a sidebar for navigation
    with st.sidebar:
        st.title(f"Welcome, {st.session_state.username}")
        
        if st.button("🏠 Home"):
            st.session_state.current_page = "Home"
            st.session_state.sidebar_state = 'collapsed'
            st.experimental_rerun()
        
        if st.button("📌 Place Finder"):
            st.session_state.current_page = "location"
            st.session_state.sidebar_state = 'collapsed'
            st.experimental_rerun()
        
        if st.button("💵 Budget tracker"):
            st.session_state.current_page = "Budjet"
            st.session_state.sidebar_state = 'collapsed'
            st.experimental_rerun()
        
        if st.button("📞 Contact"):
            st.session_state.current_page = "Contact"
            st.session_state.sidebar_state = 'collapsed'
            st.experimental_rerun()

        # Logout button
        if st.button("🚪 Log out"):
            st.session_state.authenticated = False
            st.session_state.sidebar_state = 'collapsed'
            st.experimental_rerun()

    # Main content area
    main_content = st.container()

    with main_content:
        if st.session_state.current_page == "Home":
            def get_image_with_circle(image_path):
                with open(image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode()
                    return f"""
                        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 20px;">
                            <img src="data:image/jpeg;base64,{base64_image}" style="border-radius: 50%; width: 150px; height: 150px; object-fit: cover;"/>
                        </div>
                    """

            # Load the project image
            project_image = Image.open("abc.jpg")
            st.image('index.jpg')
            st.title("Welcome to Sahayatri")
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(project_image, use_column_width=True)
            with col2:
                st.write("\n")
                st.write("\n")
                st.write("###### The premier platform designed to elevate your travel experiences with ease and convenience. Whether you're an avid explorer or a casual vacationer, SahaYatri is here to transform how you plan, experience, and enjoy your journeys.Dive into a world of possibilities with our comprehensive destination guides. From hidden gems to well-known landmarks, SahaYatri offers in-depth information, local tips, and curated recommendations to help you make the most of every location. \n We understand the struggle of finding the perfect places to visit that fit your budget.\n Whether you're looking for a quick hangout spot with friends or planning a full-blown trip, Sahayatri offers personalized recommendations based on your budget and interests.")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")

            faqs = [
                {"question": "What is SahaYatri?", "answer": "SahaYatri is a travel companion platform that helps you plan, book, and enjoy your trips with ease."},
                {"question": "How does SahaYatri work?", "answer": "SahaYatri provides tools and resources to explore destinations, plan your travel, and get personalized recommendations based on your preferences."},
                {"question": "How do I contact customer support?", "answer": "You can contact our customer support team through the 'Contact Us' section on our website or app. We offer support via email and live chat."},
            ]

            # Display FAQ section
            st.title("Frequently Asked Questions")

            for faq in faqs:
                with st.expander(faq["question"]):
                    st.write(faq["answer"])

            st.title("Our Services")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("Personalized location finder")
                st.write("Our platform connects you with expert doctors specializing in cardiovascular health.")
            with col2:
                st.success("Budget-Friendly booking")
                st.write("Learn about maintaining a healthy heart and preventing cardiovascular diseases.")
            with col3:
                st.warning("Simple design")
                st.write("Leveraging artificial intelligence to provide cutting-edge cardiac care solutions.")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")

        elif st.session_state.current_page == "Budjet":
            omg.show()

        elif st.session_state.current_page == "location":
            location.show()

        elif st.session_state.current_page == "Contact":
            contact.show()

    # Footer
    st.markdown("""
        <div class="footer">
            <div class="footer-content">
                <div class="footer-left">
                    <h3>Explore, Discover, Repeat</h3>
                    <p>Take the first step towards understanding your heart health with our AI-powered platform. Gain insights and early detection possibilities to empower your well-being. Start your journey today.</p>
                </div>
            </div>
            <hr class="horizontal-line">
            <div class="footer-bottom">
                &copy; 2024 SahaYatri, Inc. All Rights Reserved
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Scroll to top when page changes
    st.markdown('<script>scrollToTop();</script>', unsafe_allow_html=True)

# Set sidebar state
st.sidebar.markdown(f"""
    <script>
        var sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        sidebar.setAttribute('data-collapsed', '{st.session_state.sidebar_state}');
    </script>
""", unsafe_allow_html=True)
