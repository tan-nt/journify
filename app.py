import streamlit as st
from config.config import load_config
from page.about_us import display_about_us

load_config()

st.set_page_config(
    page_title="Journify",
    page_icon=":shield:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.image("resource/journify.png")
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
    


# ------------------ Main App UI ------------------ #
tab1, tab2, tab3 = st.tabs(["Home", "Exploration", "About Us"])
with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("resource/ArXiv_logo.png")
    with col3:
        st.write(' ')

    st.markdown("<h1 style='text-align: center;'>Welcome to Journify</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Explore academic articles with ease</p>", unsafe_allow_html=True)

    # CSS for the Google-style search bar
    st.markdown("""
        <style>
            .search-container {
                display: flex;
                justify-content: center;
                margin-top: 40px;
            }
            .search-bar {
                width: 60%;
                padding: 12px 20px;
                border: 2px solid #ccc;
                border-radius: 25px;
                font-size: 16px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
                outline: none;
                transition: all 0.3s ease;
            }
            .search-bar:focus {
                border-color: #3498db;
                box-shadow: 0 4px 12px rgba(0, 123, 255, 0.4);
            }
            .search-btn {
                margin-top: 20px;
                display: flex;
                justify-content: center;
                gap: 10px;
            }
            .btn {
                font-size: 16px;
                padding: 10px 20px;
                border: none;
                border-radius: 20px;
                background-color: #3498db;
                color: white;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .btn:hover {
                background-color: #2980b9;
            }
            .btn-secondary {
                background-color: #f2f2f2;
                color: #333;
            }
            .btn-secondary:hover {
                background-color: #ddd;
            }
        </style>
    """, unsafe_allow_html=True)

    # HTML structure for the search bar
    st.markdown("""
    <div class="search-container">
        <input type="text" class="search-bar" placeholder="Search for articles...">
    </div>
    <div class="search-btn">
        <button class="btn">Search Journify</button>
        <button class="btn btn-secondary">I'm Feeling Curious</button>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    display_about_us()