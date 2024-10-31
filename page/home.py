import streamlit as st
from ai_model import knn

def display_home():
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
    
    # Search input
    query = st.text_input("Search for articles...", key="search_query")

    if query:
        # Loading spinner while processing search results
        with st.spinner("Searching for articles..."):
            # Filter articles based on query
            filtered_df = knn.filter_articles(query, knn.knn, knn.tfidf, knn.df)
        
        # Show number of results
        num_results = len(filtered_df)
        st.write(f"### {num_results} results found")

        # Display filtered results
        st.subheader("Search Results")
        for idx, row in filtered_df.iterrows():
            st.write(f"**Title:** {row['title']}")
            st.write(f"**Authors:** {row['authors']}")

            # Display first 300 characters of the abstract
            short_abstract = row['abstract'][:300]
            st.write(f"**Abstract:** {short_abstract}...")

            # "Show More" expander for the full abstract
            with st.expander("View all abstract"):
                st.write(row['abstract'])  # Display full abstract
            
            st.write("---")
