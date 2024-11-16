import base64
import streamlit as st
from PIL import Image

# Function to encode images to base64
def load_image(image_file):
    try:
        with open(image_file, "rb") as file:
            return base64.b64encode(file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

# Load images
journify_logo = load_image("resource/journify_logo.png")
arxiv_logo = load_image("resource/arxiv_logo.png")

def display_introduction():
    # Title and logo
    st.markdown(
        """
        <h1 style='text-align: center;'>Welcome to Journify</h1>
        <div style="display: flex; justify-content: center; gap: 20px; margin: 10px 0;">
            <img src="data:image/png;base64,{journify_logo}" alt="Intelligent Article Explorer Logo" width="200">
        </div>
        """.format(journify_logo=journify_logo), 
        unsafe_allow_html=True
    )
    
    # Brief Introduction
    st.markdown(
        """
        **Journify** is your intelligent journal explorer powered by AI. It's designed to empower researchers, students, and curious minds with a seamless exploration of academic literature. With Journify, you can:
        
        - **Discover curated article recommendations** that offer deep insights across a wide range of topics.
        - Access our **AI-driven Q&A chatbot** for quick and accurate answers to your research queries.
        """
    )

    st.markdown("<hr style='border-top:2px dotted #888'>", unsafe_allow_html=True)

    # Benefits of Journify with interactive toggles
    st.header("Why Choose Journify?")
    if st.button("Show Benefits"):
        st.markdown(
            """
            Journify leverages cutting-edge technology to enhance your research experience:
            - **Personalized Recommendations**: Our advanced algorithms tailor article suggestions based on your interests and previous searches.
            - **Interactive Chatbot**: Get instant responses to your questions, saving you time and enhancing your understanding of complex topics.
            - **User-Friendly Interface**: Enjoy a clean, intuitive interface that allows for easy navigation and exploration.
            - **Comprehensive Resources**: Gain access to a vast database of academic articles, empowering you to make informed decisions in your research.
            """
        )

    st.markdown("<h2 style='text-align: center;'>⭐ ⭐ ⭐</h2>", unsafe_allow_html=True)
    
    # The arXiv Dataset
    st.markdown(
        """
        <div style="display: flex; justify-content: center; gap: 20px; margin: 10px 0;">
            <img src="data:image/png;base64,{arxiv_logo}" alt="Intelligent Article Explorer Logo" width="150">
        </div>
        """.format(arxiv_logo=arxiv_logo), 
        unsafe_allow_html=True
    )

    st.header("About the arXiv Dataset")
    st.markdown(
        """
        The **arXiv** dataset is a rich repository of academic papers across various domains, providing a wealth of knowledge for researchers and students. Here's a snapshot of the dataset structure:

        - **ID**: Unique identifier for each paper (e.g., `"0704.0001"`).
        - **Submitter**: The individual who submitted the paper (e.g., `"Pavel Nadolsky"`).
        - **Authors**: List of authors contributing to the paper (e.g., `"C. Balázs, E. L. Berger, P. M. Nadolsky, C.-P. Yuan"`).
        - **Title**: The title of the paper (e.g., `"Calculation of prompt diphoton production cross sections at Tevatron and LHC energies"`).
        - **Abstract**: A brief summary of the research findings, highlighting key insights and methodologies.
        - **DOI**: Digital Object Identifier for citation purposes (e.g., `"10.1103/PhysRevD.76.013009"`).
        - **Categories**: Classification of the paper within specific research fields (e.g., `"hep-ph"`).
        
        This structured format enables efficient querying and retrieval of relevant articles tailored to your research needs.
        """
    )

    st.markdown(
        """
        <div style="border-bottom: 2px solid #FFC300; animation: glow 1s ease-in-out infinite alternate;">
        </div>
        <style>
        @keyframes glow {
            from { border-color: #FFC300; }
            to { border-color: #FF5733; }
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center;'>👑 👑 👑 👑 👑</h2>", unsafe_allow_html=True)
    
    # How Journify Works with collapsible sections
    st.header("How Journify Works")
    with st.expander("Click to learn more about our technologies"):
        st.markdown(
            """
            Journify utilizes state-of-the-art technologies to deliver a personalized research experience:
            - **K-Nearest Neighbors (KNN)**: Efficient classification of subjects, allowing for relevant article recommendations.
            - **Bayesian Search**: Refined querying that enhances the quality of search results.
            - **High-Accuracy Recommendation Engines**: Implementing **HNSW-ANN** and **BERT (Weaviate)** to deliver precise article suggestions.
            - **Large Language Model (LLM) + RAG Chatbot**: For responsive and reliable answers to your research queries.

            By integrating these technologies, Journify not only simplifies the search process but also enhances the overall learning experience.
            """
        )

    st.markdown("<h2 style='text-align: center;'>✨ ✨ ✨ ✨ ✨</h2>", unsafe_allow_html=True)

    # How to Use Journify with an interactive guide
    st.header("How to Use Journify")
    guide = [
        "1. **Explore Topics**: Use the search functionality to find articles related to your area of interest.",
        "2. **Ask Questions**: Engage with our AI-driven chatbot by typing your research questions for immediate responses.",
        "3. **Discover Recommendations**: Browse curated article suggestions based on your previous interactions and interests."
    ]
    
    for step in guide:
        st.markdown(f"{step}")

    st.markdown("<h2 style='text-align: center;'>🌟🌟🌟</h2>", unsafe_allow_html=True)
    
    # Future Improvements with a slider for user feedback
    st.header("Future Improvements")
    st.markdown(
        """
        We are committed to continuously enhancing the Journify experience. Upcoming features include:
        - **Enhanced User Interface**: Improving navigation and accessibility for a seamless experience.
        - **Advanced Analytics**: Providing insights into reading patterns and topic interests.
        - **Integration with More Datasets**: Expanding our database to include more diverse academic resources.
        - **Increased Personalization**: Using machine learning to provide even more tailored recommendations.

        Stay tuned for updates as we evolve and grow!
        """
    )

    st.markdown("<h2 style='text-align: center;'>❤️ ❤️ ❤️</h2>", unsafe_allow_html=True)
    
    # Worthy Investments
    st.header("Support Journify")
    st.markdown(
        """
        Your support helps us maintain and improve Journify. Consider making a donation to aid our development efforts:
        - **Bitcoin**: [Donate via Bitcoin](#)
        - **PayPal**: [Donate via PayPal](#)

        Every contribution counts and enables us to enhance the platform for all users. Thank you for your support!
        """)

    st.markdown("<h2 style='text-align: center;'>☀️ ☀️ ☀️ ☀️ ☀️</h2>", unsafe_allow_html=True)

    # Interactive Feedback Section
    st.header("We Value Your Feedback")
    feedback = st.slider("Rate your excitement about Journify (1-10)", 1, 10, 5)
    if feedback:
        st.success(f"Thank you for your feedback! Your excitement level: {feedback}/10")

    # Closing Remark
    st.markdown(
        """
        Join us in turning learning into growth and unlock new possibilities with **Journify**. 
        Together, we can make academic exploration more accessible and enriching!
        """
    )

# Call the display function
# display_introduction()
