import streamlit as st

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