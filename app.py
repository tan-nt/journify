import streamlit as st
from page.about_us import display_about_us
from page.home import display_search
from page.introducion import display_introduction
from page.data_exploration import display_article_analysis, display_user_logger_analysis, display_sentiment_analysis
from page.recommendation import display_article_recommendation
import requests
import base64
import streamlit as st
from openai import OpenAI
import logging
import streamlit as st 
from streamlit_float import *
from config.config import load_env_variables
from database.json_to_sqlite import init_data
from database.sqlite_to_csv import export_to_csv
from database.user import user_model
import streamlit as st
from browser_detection import browser_detection_engine
from streamlit_option_menu import option_menu
from ai_model.chat import display_chat
from ai_model.prediction import display_prediction

logger = logging.getLogger()
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
logging.basicConfig(encoding="UTF-8", level=logging.INFO)

# Set Streamlit page configuration as the first command
st.set_page_config(
    page_title="Journify",
    page_icon=":shield:",
    layout="wide",
    initial_sidebar_state="expanded",
)

value = browser_detection_engine()
def log_user_access():
    def get_user_ip_address():
        try:
            response = requests.get("https://httpbin.org/get")
            data = response.json()
            ip_address = data.get("origin", "Unknown IP")
            return ip_address
        except requests.RequestException as e:
            st.error(f"Error fetching user IP address: {e}")
            return "Unknown IP"
    ip_address = get_user_ip_address()
    
    st.session_state["ip_address"] = ip_address
    user_agent = value.get("userAgent")
    st.session_state["user_agent"] = user_agent
    print(f"IP Address: {ip_address}, User agent: {user_agent}")
    user_model.upsert_user_access(ip_address, user_agent)

if "logged" not in st.session_state:
    log_user_access()
    st.session_state["logged"] = True  # Ensures this runs only once per session

# Cache the configuration loading function
@st.cache_data
def load_config():
    # Run all setup steps only once
    load_env_variables()
    init_data()
    export_to_csv()
    return "Config loaded"
# Call the cached load_config function
config_status = load_config()

st.markdown("""
    <style>
    .st-emotion-cache-1jicfl2, .st-emotion-cache-7tauuy {
        padding: 0rem 2rem 10rem !important;
    }
    </style>
""", unsafe_allow_html=True)

def display_main_tabs():
    tab1, tab2, tab3, tab4 = st.tabs(["Search", "Article Recommendation", "Data Exploration", "About Us"])
    with tab1:
        display_search()
    with tab2:
        display_article_recommendation()
    with tab3:
        st.header("Data Exploration Session")
        analysis_tab, user_log_tab, sentiment_analysis_tab = st.tabs(["Article Analysis", "User Analysis", "Sentiment analysis"])
        with analysis_tab:
            display_article_analysis()  # Call article analysis function
        with user_log_tab:
            display_user_logger_analysis()  # Call user analysis function
        with sentiment_analysis_tab:
            display_sentiment_analysis()  # Call user analysis function
    with tab4:
        display_about_us()

# Initialize session state if not already set
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Function to encode images to base64
def load_image(image_file):
    try:
        with open(image_file, "rb") as file:
            return base64.b64encode(file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

journify_logo = load_image("resource/journify_logo.png")

# st.sidebar.image("resource/journify.png")
# Centered Logo and Additional Sidebar Content
if journify_logo is None:
    st.error("Logo file not found!")
else:
    st.sidebar.markdown(
        """
        <div style="display: flex; justify-content: center; gap: 20px; margin: 10px 0;">
            <img src="data:image/png;base64,{journify_logo}" alt="Intelligent Article Explorer Logo" width="200">
        </div>
        """.format(journify_logo=journify_logo), 
        unsafe_allow_html=True
    )

st.sidebar.header("Navigation")
# Create a stylish sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title=None,  # Remove the redundant menu title
        # options=["🏠 Home", 👋 Introduction", "💬 Go Chat", "🔮 Prediction", "🤖 AI Model Exploration"],
        # icons=["house", "chat-dots", "graph-up", "robot"],  # Optional icons for each menu item
        options=["🏠 Home", "👋 Introduction", "💬 Go Chat", "🔮 Prediction"],
        icons=["house", "person-circle", "chat-dots", "graph-up"],  # Optional icons for each menu item
        menu_icon="cast",  # Icon for the menu itself
        default_index=0,  # Default selected option
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f2f6"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#02ab21"},
        },
    )

# Update session state based on the selected menu option
if selected == "🏠 Home":
    st.session_state["page"] = "home"
elif selected == "👋 Introduction":
    st.session_state["page"] = "introduction"
elif selected == "💬 Go Chat":
    st.session_state["page"] = "chat"
elif selected == "🔮 Prediction":
    st.session_state["page"] = "prediction"
# elif selected == "🤖 AI Model Exploration":
#     st.session_state["page"] = "ai-exploration"


# Display content based on the current page
if st.session_state["page"] == "home":
    st.title("Welcome to the Home Page!")
    # Add your home page content here
elif st.session_state["page"] == "introduction":
    st.sidebar.markdown(
        """
        <div style='text-align: center;'>
        <h1>🌱 Welcome to Journify 🌱</h1>
        <div>
        """, unsafe_allow_html=True
    )
elif st.session_state["page"] == "chat":
    st.title("Let's ask any research-related questions!")
    # Add your chat page content here
elif st.session_state["page"] == "prediction":
    st.title("Go to predict trends!")

# Sidebar navigation and page state
if "page" not in st.session_state:
    st.session_state.page = "home"  # Default to home page
    
# Render content based on the current page
if st.session_state.page == "home":
    display_main_tabs()
elif st.session_state.page == "introduction":
    display_introduction()
elif st.session_state.page == "chat":
    display_chat()
elif st.session_state.page == "prediction":
    display_prediction()

st.sidebar.header("About")

# Brief, engaging description with emojis and enhanced formatting
st.sidebar.markdown(
    """
    <div style='text-align: center;'>
    <h1>🌱 Welcome to Journify 🌱</h1>
    <div>
    """, unsafe_allow_html=True
)
st.sidebar.markdown(
    """
    <div style='text-align: justify;'>
    Your intelligent journal explorer powered by AI. Journify empowers scholars and curious minds by providing:
    <ul>
        <li>🔍 <strong>Curated Article Recommendations</strong> across a wide range of topics.</li>
        <li>🤖 <strong>AI-driven Q&A Chatbot</strong> for quick, accurate answers to your research questions.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True
)

st.sidebar.markdown("---")

# Vision and Mission Statement
st.sidebar.markdown(
    """
    <div style='text-align: center;'>
    <h2>🚀 Learning into Lifelong Growth 🚀</h2>
    <strong>Journify</strong> is to support your journey toward academic excellence.<br> 
    <em>Join us in unlocking new possibilities through knowledge and innovation.</em>
    </div>
    """, unsafe_allow_html=True
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <div style='text-align: center;'>
        <h3>⭐ Explore, Learn, and Grow with Journify! ⭐</h3>
    </div>
    """, unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <div style='text-align: center;'>
        <a href="https://github.com/tan-nt/real-life-streamlit-app">
            <img src="https://img.shields.io/github/stars/tan-nt/real-life-streamlit-app?style=social" alt="Star on GitHub">
        </a>
    </div>
    """, unsafe_allow_html=True
)

st.sidebar.markdown("---")

# FAQ Section with collapsible details for interactivity
st.sidebar.header("FAQs")
with st.sidebar.expander("What is Journify?"):
    st.write("Journify is a platform that leverages AI to recommend articles and answer research questions, providing you with an academic companion for discovery and insight.")

with st.sidebar.expander("How does Journify work?"):
    st.write("Using advanced algorithms such as KNN classification, Bayesian search, and recommendation models, Journify personalizes high-accuracy content based on your research needs.")

with st.sidebar.expander("Is my data stored?"):
    st.write("No, all queries are processed in real-time and deleted at the session's end to ensure privacy.")

with st.sidebar.expander("Why might responses take some time?"):
    st.write("Complex queries require additional processing time. Free-tier users may experience some delay due to system limits.")

st.sidebar.markdown("---")
st.sidebar.markdown("📘 **Tips for Best Results**: Provide detailed questions for more accurate recommendations and improved insights.")
    
