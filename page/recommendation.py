import streamlit as st
from database.article import article as db_article

def display_article_recommendation():
    st.title("📚 Article Recommendations")
    st.write("Explore articles tailored to your interests. Here are some top picks for you!")

    # Recommended Articles Section
    st.markdown("### 🎯 Recommended Articles for You")
    articles = [
        {"title": "Machine Learning 101", "abstract": "An introduction to the basics of machine learning.", "url": "#"},
        {"title": "Deep Dive into Neural Networks", "abstract": "Exploring the layers of neural networks.", "url": "#"},
        {"title": "Data Science in 2024", "abstract": "Trends and predictions for data science in the upcoming years.", "url": "#"}
    ]

    col1, col2, col3 = st.columns(3)

    for idx, article in enumerate(articles):
        with (col1 if idx % 3 == 0 else col2 if idx % 3 == 1 else col3):
            st.markdown(f"#### [{article['title']}]({article['url']})")
            st.write(article["abstract"])
            st.button("Read more", key=f"rec_read_more_{idx}")

    # Top/Popular Articles Section
    st.markdown("### 🔥 Top/Popular Articles")
    top_articles = db_article.get_top_article(10)
        
    # Streamlit layout
    # st.markdown("<h2 style='text-align: center;'>🔥 Top/Popular Articles</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    # Define CSS style for a more refined "Read more" button and article layout
    st.markdown("""
        <style>
        .article-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            margin: 5px 0;
            height: 250px; /* Fixed height for uniform layout */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background-color: #fafafa;
        }
        .article-title {
            font-size: 16px;
            font-weight: bold;
            color: #1a73e8;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            text-overflow: ellipsis;
        }
        .article-abstract {
            font-size: 14px;
            color: #333;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2; /* Limits abstract to 2 lines */
            -webkit-box-orient: vertical;
            text-overflow: ellipsis;
            margin-top: 5px;
        }
        .read-more {
            display: inline-block;
            padding: 5px 12px;
            font-size: 13px;
            color: #555;
            border: 1px solid #ccc;
            border-radius: 6px;
            text-align: center;
            text-decoration: none;
            cursor: pointer;
            transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
            margin-top: auto;
        }
        .read-more:hover {
            background-color: #eee;
            color: #333;
            box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # Loop through articles and display each one in a column
    for idx, article in enumerate(top_articles):
        with (col1 if idx % 3 == 0 else col2 if idx % 3 == 1 else col3):
            st.markdown(f"""
                <div class="article-card">
                    <div class="article-title">
                        <a href="https://arxiv.org/abs/{article.get("id")}" target="_blank">
                            {article['title']}
                        </a>
                    </div>
                    <div style="font-size: 12px; color: #888; margin-top: 5px;">Cited by: {article.get("influential_citation_count")}</div>
                    <div class="article-abstract">
                        {article['abstract']}
                    </div>
                    <a href="https://arxiv.org/abs/{article.get("id")}" target="_blank" class="read-more">Read more</a>
                </div>
            """, unsafe_allow_html=True)

    # Other Friends Recommend Section
    st.markdown("### 👥 Other Friends Recommend for You")
    friend_recommendations = [
        {"title": "AI Ethics and Society", "abstract": "Examining the ethical implications of AI advancements.", "url": "#"},
        {"title": "Data Visualization Techniques", "abstract": "Learn about effective data visualization for insights.", "url": "#"},
        {"title": "Future of Quantum Computing", "abstract": "Exploring how quantum computing will transform industries.", "url": "#"}
    ]

    col1, col2, col3 = st.columns(3)

    for idx, article in enumerate(friend_recommendations):
        with (col1 if idx % 3 == 0 else col2 if idx % 3 == 1 else col3):
            st.markdown(f"#### [{article['title']}]({article['url']})")
            st.write(article["abstract"])
            st.button("Read more", key=f"friend_rec_read_more_{idx}")
