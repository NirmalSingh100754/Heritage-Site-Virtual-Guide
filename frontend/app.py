from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pymongo
from urllib.parse import quote_plus
import certifi
import os

# Import our utilities and components
from utils.api_client import api_client
from utils.session_state import init_session_state, clear_analysis
from components.featured_cards import display_featured_cards
from components.image_upload import handle_image_upload
from components.search_component import handle_search

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Heritage Virtual Guide",
    layout="wide",
    page_icon="🏛️"
)

# ===================== CUSTOM DARK CSS =====================
dark_css = """
<style>
/* Background */
.stApp {
    background: linear-gradient(to right, #0f0f0f, #1a1a1a);
    font-family: 'Georgia', serif;
    color: #e0d5c0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #121212;
    color: #e0d5c0;
}
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 {
    color: #f0c674;
}

/* Titles */
h1, h2, h3 {
    color: #f0c674;
    font-weight: bold;
    text-align: center;
    text-shadow: 1px 1px 4px #000;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(145deg, #f0c674, #d4a017);
    color: black;
    border-radius: 10px;
    padding: 8px 20px;
    border: none;
    font-weight: bold;
}
.stButton>button:hover {
    background: linear-gradient(145deg, #d4a017, #b8860b);
    color: white;
}

/* Forms */
.stTextInput>div>div>input {
    border-radius: 8px;
    border: 1px solid #f0c674;
    padding: 6px;
    background-color: #222;
    color: #f5f5f5;
}
.stTextInput>div>label {
    font-weight: bold;
    color: #f0c674;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 30px;
    justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    font-size: 16px;
    font-weight: bold;
    color: #e0d5c0;
}
.stTabs [aria-selected="true"] {
    border-bottom: 3px solid #f0c674 !important;
    color: #f0c674 !important;
}

/* Cards */
.card {
    background: #1c1c1c;
    border: 1px solid #f0c674;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 2px 4px 15px rgba(0,0,0,0.6);
    transition: transform 0.2s ease;
}
.card:hover {
    transform: translateY(-2px);
    box-shadow: 4px 6px 20px rgba(240, 198, 116, 0.3);
}

/* Scrollable content */
.scrollable-content {
    max-height: 400px;
    overflow-y: auto;
    padding-right: 10px;
}
.scrollable-content::-webkit-scrollbar {
    width: 8px;
}
.scrollable-content::-webkit-scrollbar-track {
    background: #1a1a1a;
    border-radius: 4px;
}
.scrollable-content::-webkit-scrollbar-thumb {
    background: #f0c674;
    border-radius: 4px;
}
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)

# ===================== INITIALIZE SESSION STATE =====================
init_session_state()

# ===================== DATABASE CONFIG =====================
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "indranilsamanta2003")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_CLUSTER = os.getenv("MONGODB_CLUSTER")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

@st.cache_resource
def init_connection():
    try:
        username = quote_plus(MONGODB_USERNAME)
        password = quote_plus(MONGODB_PASSWORD)
        connection_string = f"mongodb+srv://{username}:{password}@{MONGODB_CLUSTER}/{MONGODB_DATABASE}?retryWrites=true&w=majority&appName=ClusterHeritage"
        client = pymongo.MongoClient(connection_string, tlsCAFile=certifi.where())
        client.admin.command('ping')
        st.sidebar.success("✅ Connected to MongoDB successfully!")
        return client
    except Exception as e:
        st.sidebar.error(f"❌ MongoDB connection failed: {str(e)}")
        return None

client = init_connection()
if client:
    db = client[MONGODB_DATABASE]
    users_collection = db.users
else:
    class DummyCollection:
        def find_one(self, *args, **kwargs): return None
        def insert_one(self, *args, **kwargs): return {"inserted_id": "demo_id"}
    users_collection = DummyCollection()
    st.sidebar.warning("⚠️ Running in demo mode without database connection.")

# ===================== BACKEND STATUS =====================
if api_client.health_check():
    st.sidebar.success("✅ Backend API Connected")
else:
    st.sidebar.error("🚫 Backend API Not Connected")

# ===================== AUTH FUNCTIONS =====================
def login_user(username, password):
    if not client:
        return bool(username and password)
    user = users_collection.find_one({"username": username, "password": password})
    return user is not None

def signup_user(username, password, email):
    if not client:
        if not username or not password or not email:
            return False, "All fields are required"
        return True, "User created successfully! (Demo mode)"
    if users_collection.find_one({"username": username}):
        return False, "Username already exists"
    users_collection.insert_one({"username": username, "password": password, "email": email})
    return True, "User created successfully!"

# ===================== MAIN UI =====================
if not st.session_state.authenticated:
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab1:
        st.subheader("Login to Your Guide")
        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Login")
            if login_submitted:
                if login_user(login_username, login_password):
                    st.session_state.authenticated = True
                    st.session_state.username = login_username
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")

    with tab2:
        st.subheader("Create an Account")
        with st.form("signup_form"):
            signup_username = st.text_input("Choose a Username")
            signup_email = st.text_input("Email")
            signup_password = st.text_input("Choose a Password", type="password")
            signup_submitted = st.form_submit_button("Sign Up")
            if signup_submitted:
                success, message = signup_user(signup_username, signup_password, signup_email)
                if success:
                    st.success(message)
                else:
                    st.error(message)

else:
    
    st.sidebar.title(f"🌟 Welcome, {st.session_state.username}!")
    
    # Sidebar controls
    if st.sidebar.button("🔄 Clear History", use_container_width=True):
        clear_analysis()
        st.session_state.chat_history = []
        st.success("History cleared!")
        
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.chat_history = []
        st.session_state.uploaded_image = None
        st.session_state.analysis_result = None
        st.rerun()
    
    # Main title
    st.title("🏛️ Heritage Virtual Guide")
    st.markdown("<p style='text-align:center; font-size:18px; color:#f0c674;'>Discover the history and stories behind the world's greatest heritage sites.</p>", unsafe_allow_html=True)
    
    # Main tabs
    tab_home, tab_search, tab_upload = st.tabs(["🏠 Home", "🔍 Search", "🖼️ Upload Image"])
    
    with tab_home:
        st.header("✨ Featured Heritage Sites")
        
        # Get recommendations from backend
        with st.spinner("Loading recommendations..."):
            recommendations = api_client.get_recommendations()
        
        if recommendations:
            display_featured_cards(recommendations)
        else:
            st.info("🌟 Loading featured heritage sites...")
            
        # Additional info
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class='card'>
                <h3>🎯 How It Works</h3>
                <p>• Upload images of heritage sites for AI analysis</p>
                <p>• Search for any historical monument</p>
                <p>• Get detailed historical information</p>
                <p>• Discover nearby attractions</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='card'>
                <h3>📚 Features</h3>
                <p>• AI-powered image recognition</p>
                <p>• Comprehensive historical data</p>
                <p>• Visitor information & tips</p>
                <p>• Interactive exploration</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab_search:
        handle_search()
    
    with tab_upload:
        handle_image_upload()