import streamlit as st
from page.about_us import display_about_us
from page.home import display_search
from page.data_exploration import display_article_analysis, display_user_logger_analysis
from page.recommendation import display_article_recommendation
import requests
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
        analysis_tab, user_log_tab = st.tabs(["Article Analysis", "User Analysis"])
        with analysis_tab:
            display_article_analysis()  # Call article analysis function
        with user_log_tab:
            display_user_logger_analysis()  # Call user analysis function
    with tab4:
        display_about_us()

# Initialize session state if not already set
if "page" not in st.session_state:
    st.session_state["page"] = "home"

st.sidebar.image("resource/journify.png")
st.sidebar.header("Navigation")
# Create a stylish sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title=None,  # Remove the redundant menu title
        options=["🏠 Home", "💬 Go Chat"],
        icons=["house", "chat-dots"],  # Optional icons
        menu_icon="cast",  # Menu icon
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
elif selected == "💬 Go Chat":
    st.session_state["page"] = "chat"

# Display content based on the current page
if st.session_state["page"] == "home":
    st.title("Welcome to the Home Page!")
    # Add your home page content here
elif st.session_state["page"] == "chat":
    st.title("Let's Chat!")
    # Add your chat page content here

# Sidebar navigation and page state
if "page" not in st.session_state:
    st.session_state.page = "home"  # Default to home page
    
# Render content based on the current page
if st.session_state.page == "home":
    display_main_tabs()
elif st.session_state.page == "chat":
    display_chat()

st.sidebar.header("How to use Journify")
st.sidebar.header("About")

with st.sidebar:
    st.markdown(
        "Welcome to **Journify** (Intelligent Journal Explorer), an AI-powered platform designed to provide users with curated article recommendations and an intelligent Q&A chatbot for arXiv papers."
    )
    st.markdown(
        """
        Journify leverages advanced AI models to deliver relevant content and insights. Our platform combines multiple state-of-the-art techniques, such as:
        - **KNN** for subject classification and filtering.
        - **Bayesian Search** for intelligent querying.
        - **HNSW-ANN and BERT (Weaviate)** for high-accuracy recommendation systems.
        - **LLM + RAG** for Q&A with our chatbot, providing quick, reliable answers to your research questions.
        """
    )
    st.markdown("Created by the Journify Team.")
    # Add "Star on GitHub" link to the sidebar
    st.sidebar.markdown(
        "⭐ Star on GitHub: [![Star on GitHub](https://img.shields.io/github/stars/tan-nt/real-life-streamlit-app?style=social)](https://github.com/tan-nt/real-life-streamlit-app)"
    )
    st.markdown("""---""")

# Add "FAQs" section to the sidebar
st.sidebar.header("FAQs")
with st.sidebar:
    st.markdown(
        """
    ### **What is Journify?**
    Journify is an intelligent journal exploration tool designed to recommend the best articles and answer queries from arXiv using AI. It combines various machine learning techniques to provide relevant, curated content and a seamless research experience.
    """
    )
    st.markdown(
        """
    ### **How does Journify work?**
    Journify utilizes a combination of KNN for classification, Bayesian methods for search, HNSW-ANN and BERT (via Weaviate) for recommendations, and an LLM + RAG-based chatbot to deliver efficient and accurate recommendations and insights.
    """
    )
    st.markdown(
        """
    ### **Do you store the queries or recommendations?**
    No, Journify does not store any personal data or queries. All interactions are temporary and are cleared after the session ends.
    """
    )
    st.markdown(
        """
    ### **Why does it take time to generate recommendations or answer queries?**
    Processing can vary based on query complexity and system load. Free users may experience slower response times due to rate limits. Consider using a paid tier for faster responses.
    """
    )
    st.markdown(
        """
    ### **Are recommendations and answers always accurate?**
    While Journify uses advanced models, results may not be 100% accurate. Machine learning models like BERT and LLMs can sometimes misinterpret or 'hallucinate' content. We recommend using Journify's output as a guide and verifying with additional sources if needed.
    """
    )
    st.markdown(
        """
    ### **How can I get the best recommendations and answers?**
    Provide detailed queries and specify topics clearly. The more context you give, the more relevant and accurate the recommendations and responses from Journify will be.
    """
    )
    