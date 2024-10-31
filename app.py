import streamlit as st
from config.config import load_config
from page.about_us import display_about_us
from page.home import display_home
from page.data_exploration import display_data_exploration

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
tab1, tab2, tab3, tab4 = st.tabs(["Home", "Article recommendation", "Data exploration", "About Us"])
with tab1:
    display_home()
with tab3:
    display_data_exploration()
with tab4:
    display_about_us()
