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

    # Fetch top articles (assuming db_article.get_top_article(10) is defined and working)
    top_articles = db_article.get_top_article(10)

    # Streamlit layout
    st.markdown("<h2 style='text-align: center;'>🔥 Top/Popular Articles</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    # Define enhanced CSS styles for the article card
    st.markdown("""
        <style>
        .article-card {
            position: relative;
            border: none;
            border-radius: 12px;
            overflow: hidden;
            margin: 10px 0;
            height: 380px; /* Adjusted height for image inclusion */
            display: flex;
            flex-direction: column;
            background-color: #ffffff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease;
        }
        .article-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        .article-image {
            width: 100%;
            height: 180px;
            object-fit: cover;
        }
        .article-content {
            padding: 15px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }
        .article-title {
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            text-overflow: ellipsis;
        }
        .article-abstract {
            font-size: 14px;
            color: #555;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 3; /* Limits abstract to 3 lines */
            -webkit-box-orient: vertical;
            text-overflow: ellipsis;
            flex-grow: 1;
        }
        .article-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
        }
        .cited-count {
            font-size: 12px;
            color: #888;
        }
        .read-more {
            padding: 6px 12px;
            font-size: 13px;
            color: #333;
            border: 1px solid #ccc;
            border-radius: 6px;
            text-decoration: none;
            cursor: pointer;
            transition: border-color 0.3s ease, color 0.3s ease;
        }
        .read-more:hover {
            border-color: red;
            color: red;
        }
        </style>
    """, unsafe_allow_html=True)

    # Define a placeholder image URL for when no specific image is available
    # default_image_url = "https://via.placeholder.com/800x600?text=No+Image+Available"
    default_image_url = "https://librarylearningspace.com/wp-content/uploads/2022/05/arxiv-logo-1.png"

    # Loop through articles and display each one in a column
    for idx, article in enumerate(top_articles):
        with (col1 if idx % 3 == 0 else col2 if idx % 3 == 1 else col3):
            # Check if there's an image link available, otherwise use the default image
            image_url = article.get("image_link", default_image_url)
            st.markdown(f"""
                <div class="article-card">
                    <img src="{image_url}" alt="Article Image" class="article-image">
                    <div class="article-content">
                        <div class="article-title">
                            <a href="https://arxiv.org/abs/{article.get("id")}" target="_blank" style="text-decoration: none; color: inherit;">
                                {article['title']}
                            </a>
                        </div>
                        <div class="article-abstract">
                            {article['abstract']}
                        </div>
                        <div class="article-footer">
                            <div class="cited-count">Cited by: {article.get("influential_citation_count", "N/A")}</div>
                            <a href="https://arxiv.org/abs/{article.get("id")}" target="_blank" class="read-more">Read more</a>
                        </div>
                    </div>
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
