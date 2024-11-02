import streamlit as st

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
    top_articles = [
        {"title": "Understanding Artificial Intelligence", "abstract": "An overview of AI and its applications in modern technology.", "url": "#"},
        {"title": "Top Data Science Tools for 2024", "abstract": "Discover the best tools and software for data scientists this year.", "url": "#"},
        {"title": "The Evolution of Machine Learning", "abstract": "Tracing the journey of ML from its beginnings to the present.", "url": "#"}
    ]

    col1, col2, col3 = st.columns(3)

    for idx, article in enumerate(top_articles):
        with (col1 if idx % 3 == 0 else col2 if idx % 3 == 1 else col3):
            st.markdown(f"#### [{article['title']}]({article['url']})")
            st.write(article["abstract"])
            st.button("Read more", key=f"top_read_more_{idx}")

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
