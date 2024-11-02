import streamlit as st
from database.article import article_model as db_article
from ai_model.recommendation import hybrid_recommendation_of_content_collaborative_filtering, other_friends_recommend

def display_article_recommendation():
    # Define a placeholder image URL for when no specific image is available
    # default_image_url = "https://via.placeholder.com/800x600?text=No+Image+Available"
    default_image_url = "https://librarylearningspace.com/wp-content/uploads/2022/05/arxiv-logo-1.png"
    
    st.title("📚 Article Recommendations")
    st.write("Explore articles tailored to your interests. Here are some top picks for you!")

    # Recommended Articles Section
    st.markdown("### 🎯 Recommended Articles for You")

    recommended_articles = hybrid_recommendation_of_content_collaborative_filtering(
        st.session_state.get("ip_address") or "",
        num_recommendations=5)

    col1, col2, col3 = st.columns(3)
    for idx, article in enumerate(recommended_articles):
        with (col1 if idx % 3 == 0 else col2 if idx % 3 == 1 else col3):
            # Check if there's an image link available, otherwise use the default image
            image_url = article.get("image_link", default_image_url)
            st.markdown(f"""
                <div class="article-card">
                    <img src="{image_url}" alt="Article Image" class="article-image">
                    <div class="article-content">
                        <div class="article-title">
                            <a href="https://arxiv.org/abs/{article.get("article_id")}" target="_blank" style="text-decoration: none; color: inherit;">
                                {article['title']}
                            </a>
                        </div>
                        <div class="article-abstract">
                            {article['abstract']}
                        </div>
                        <div class="article-footer">
                            <div class="cited-count">Cited by: {article.get("influential_citation_count", "0")}</div>
                            <a href="https://arxiv.org/abs/{article.get("article_id")}" target="_blank" class="read-more">Read more</a>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Streamlit layout
    st.markdown("### 🔥 Top/Popular Articles")
    # Fetch top articles (assuming db_article.get_top_article(10) is defined and working)
    top_articles = db_article.get_top_article(10)
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
            height: 400px; /* Adjusted height for image inclusion */
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
                            <div class="cited-count">Cited by: {article.get("influential_citation_count", "0")}</div>
                            <a href="https://arxiv.org/abs/{article.get("id")}" target="_blank" class="read-more">Read more</a>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Other Friends Recommend Section
    st.markdown("### 👥 Other Friends Recommend for You")
    recommended_articles = other_friends_recommend(
        st.session_state["ip_address"],
        num_recommendations=5)
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
            height: 400px; /* Adjusted height for image inclusion */
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

    # Loop through articles and display each one in a column
    for idx, article in enumerate(recommended_articles):
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
                            <div class="cited-count">Cited by: {article.get("influential_citation_count", "0")}</div>
                            <a href="https://arxiv.org/abs/{article.get("id")}" target="_blank" class="read-more">Read more</a>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
