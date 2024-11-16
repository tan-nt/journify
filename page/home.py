import streamlit as st
from ai_model import search
from database.user_access_log import user_access_logger_model
import random
from datetime import datetime, timedelta
import pandas as pd

# Define a function to determine relevance based on the score
# Define a function to determine relevance and style based on the score
def get_relevance_label_and_style(score):
    if score < 0.3:
        return "LOW RELEVANCE", "background-color: #FF4C4C; color: white; border-radius: 5px; padding: 5px 10px;"
    elif 0.3 <= score < 0.7:
        return "MEDIUM RELEVANCE", "background-color: #FFD700; color: black; border-radius: 5px; padding: 5px 10px;"
    else:
        return "HIGH RELEVANCE", "background-color: #4CAF50; color: white; border-radius: 5px; padding: 5px 10px;"

def display_search():
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
    
    st.write("### Top 5 Popular Keywords")
    # Example popular keywords
    popular_keywords = ["Quark Model", "languages", "physical laws", "Quantum", "Kiz function"]

    # Session state to hold the selected keyword
    if "selected_keyword" not in st.session_state:
        st.session_state.selected_keyword = ""

    # Display popular keywords above the search bar
    cols = st.columns(len(popular_keywords))  # Create a column for each keyword

    for col, keyword in zip(cols, popular_keywords):
        with col:
            if st.button(f"🔍 {keyword}"):
                st.session_state.selected_keyword = keyword
    
    # Search bar prefilled with the selected keyword
    query = st.text_input(
        "Search for articles...",
        value=st.session_state.selected_keyword,  # Prefill the search bar
        key="search_query"
    )

    if query:
        # Loading spinner while processing search results
        with st.spinner("Searching for articles..."):
            # Filter articles based on query
            knn_filtered_df = search.filter_articles_knn(query, search.knn, search.tfidf, search.df)
            hnsw_filtered_df = search.filter_articles_hnsw(query, search.index, search.model, search.hnsw_df)
            # Combine KNN and HNSW filtered results
            combined_df = pd.concat([knn_filtered_df, hnsw_filtered_df], ignore_index=True)                
            # Deduplicate articles based on 'title' column
            filtered_df = combined_df.drop_duplicates(subset='title', keep='first')
        
        # Show number of results
        num_results = len(filtered_df)
        # Initialize counters for relevance categories
        low_relevance_count = 0
        medium_relevance_count = 0
        high_relevance_count = 0
        
        # Iterate through the dataframe to calculate counts and display results
        for _, row in filtered_df.iterrows():
            relevance_label, _ = get_relevance_label_and_style(row['score'])

            # Increment counters based on relevance
            if relevance_label == "LOW RELEVANCE":
                low_relevance_count += 1
            elif relevance_label == "MEDIUM RELEVANCE":
                medium_relevance_count += 1
            elif relevance_label == "HIGH RELEVANCE":
                high_relevance_count += 1
        
        st.write(f"### {num_results} results found")
        st.markdown(
            f"""
            - **High Relevance:** {high_relevance_count}
            - **Medium Relevance:** {medium_relevance_count}
            - **Low Relevance:** {low_relevance_count}
            """
        )

        # Display filtered results
        st.subheader("Search Results")
        for idx, row in filtered_df.iterrows():
            st.write(f"**Title:** {row['title']}")
            st.write(f"**Authors:** {row['authors']}")
            
              # Display clickable link to open the newspaper
            if 'article_id' in row and row['article_id']:
                st.markdown(f"[**Read Full Article**](https://arxiv.org/abs/{row['article_id']})", unsafe_allow_html=True)

            # Display first 300 characters of the abstract
            short_abstract = row['abstract'][:300]
            st.write(f"**Abstract:** {short_abstract}...")
            
              # Get relevance label and style
            relevance_label, style = get_relevance_label_and_style(row['score'])
            st.markdown(
                f'<span style="{style}">{relevance_label}</span>',
                unsafe_allow_html=True,
            )
            
            st.write(f"**Searching model:** {row['model']}")
            st.write(f"**Cosine similarity score :** {row['score']}")

            # "Show More" expander for the full abstract
            with st.expander("View all abstract"):
                st.write(row['abstract'])  # Display full abstract
                
                   # Retrieve and display user comments/feedback
            comments = get_comments(row['article_id'])  # Replace this with your actual comments retrieval method
            if comments:
                for comment in comments:
                    # HTML structure for each comment with sentiment
                    sentiment_color = sentiment_colors.get(comment['sentiment'], "#808080")
                    st.markdown(f"""
                    <div style="display: flex; align-items: start; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px;">
                        <div style="background-color: #333; color: white; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-size: 1.2em; margin-right: 10px;">
                            {comment['username'][0].upper()}
                        </div>
                        <div style="flex-grow: 1;">
                            <p style="font-weight: bold; font-size: 1em; margin: 0;">{comment['username']}</p>
                            <p style="color: #555; font-size: 0.9em; margin: 0;">{comment['date']}</p>
                            <p style="font-size: 1em; margin: 5px 0;">{comment['text']}</p>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <span style="background-color: {sentiment_color}; color: white; padding: 5px 10px; border-radius: 5px; font-size: 0.8em; font-weight: bold;">{comment['sentiment']}</span>
                                <button style="background: none; border: none; color: #888; cursor: pointer;">👍 {comment.get('likes', 0)}</button>
                                <button style="background: none; border: none; color: #888; cursor: pointer;">👎 {comment.get('dislikes', 0)}</button>
                                <button style="background: none; border: none; color: #888; cursor: pointer;">Reply</button>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("No comments yet.")
            
            user_access_logger_model.log_action(
                ip_address=st.session_state.get("ip_address"),
                article_id=row.get("article_id"),
                action_type="search",
                title=row.get("title"),
                abstract=row.get("abstract"),
                influential_citation_count=row.get("influential_citation_count"),
                search_query=row.get("query"),
            )
            st.write("---")


# Predefined comments categorized by sentiment
predefined_comments = {
    "Positive": [
        "This article was very insightful!",
        "Great research, thanks for sharing!",
        "Helpful for my own studies, thanks!",
        "Impressive work! Learned a lot from this article.",
        "The findings are extremely valuable. Well done!"
    ],
    "Neutral": [
        "Interesting approach, but needs more clarity.",
        "This research has potential, but I need more details.",
        "Good article, but I'm not entirely convinced.",
        "Some points are valid, but others require more evidence.",
        "It's okay, but I expected more depth."
    ],
    "Negative": [
        "I found the methodology a bit unclear.",
        "This article lacks substantial evidence.",
        "Not very informative.",
        "I disagree with the conclusions drawn.",
        "The article did not meet my expectations."
    ]
}

# Function to retrieve comments with predefined sentiment based on the comment text
def get_comments(article_id):
    # Generate a random number of comments for demonstration
    num_comments = random.randint(0, 5)
    comments = []
    
    for _ in range(num_comments):
        # Randomly assign sentiment
        sentiment = random.choice(["Positive", "Neutral", "Negative"])
        
        # Select a comment text based on the sentiment
        text = random.choice(predefined_comments[sentiment])
        
        # Generate random username and other details
        username = random.choice(["user123", "researcherA", "student98", "prof_smith", "analyst007"])
        date = datetime.now() - timedelta(days=random.randint(1, 30))  # Random date within the past month
        likes = random.randint(0, 100)
        
        comments.append({
            "username": username,
            "text": text,
            "date": date.strftime("%Y-%m-%d"),
            "sentiment": sentiment,
            "likes": likes,
            "dislikes": random.randint(0, 20)
        })
    
    return comments

# Sentiment color mapping
sentiment_colors = {
    "Positive": "#4CAF50",  # Green
    "Neutral": "#FF9800",   # Orange
    "Negative": "#F44336"   # Red
}