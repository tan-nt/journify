import streamlit as st
from streamlit.components.v1 import html

# Define a function to display the "About Us" section
def display_about_us():
    # Team member data
    team_members = [
        {
            "name": "Huỳnh Thanh Tân",
            "role": "Machine Learning Developer",
            "bio": "Tân has 1 year of experience in data science and specializes in NLP and recommendation systems.",
        },
        {
            "name": "Trần Quốc Thái",
            "role": "Data Developer",
            "bio": "Thái is a data wizard who ensures our systems run smoothly and efficiently with scalable infrastructure.",
        },
        {
            "name": "Trần Vũ Hồng Thiên",
            "role": "Machine Learning Developer",
            "bio": "With a deep passion for machine learning, Thiên focuses on developing robust models for recommendations.",
        },
        {
            "name": "Rehman Ibtasam",
            "role": "Data Developer",
            "bio": "Ibtasam designs intuitive and visually appealing data interfaces to make the Journify experience seamless.",
        }
    ]

    # CSS and HTML for team member cards and additional information
    html_content = """
    <style>
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 30px;
            padding: 20px;
        }
        .row {
            display: flex;
            gap: 40px;
            justify-content: space-evenly;
            width: 100%;
        }
        .profile-card {
            background: #f9f9f9;
            border-radius: 15px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
            overflow: hidden;
            transition: 0.3s ease;
            width: 260px;
            padding: 20px;
            text-align: center;
            font-family: Arial, sans-serif;
        }
        .profile-card:hover {
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
            transform: translateY(-8px);
        }
        .profile-card h3 {
            margin: 15px 0 10px;
            font-size: 1.6em;
            color: #333;
        }
        .profile-card p {
            color: #666;
            font-size: 1em;
            margin: 0 10px 15px;
            line-height: 1.4em;
        }
        .info-section {
            text-align: center;
            font-family: Arial, sans-serif;
            margin-top: 40px;
        }
        .info-section h3 {
            font-size: 1.8em;
            margin-bottom: 10px;
        }
        .info-section p {
            font-size: 1em;
            margin: 5px 0;
            color: #555;
        }
        .info-section a {
            color: #3498db;
            text-decoration: none;
        }
        .info-section a:hover {
            color: #2980b9;
            text-decoration: underline;
        }
    </style>
    
    <!-- Team Member Cards -->
    <div class='container'>
    """

    # Generate HTML for each team member in two-member rows
    for i in range(0, len(team_members), 2):
        html_content += "<div class='row'>"
        for member in team_members[i:i+2]:  # Two members per row
            html_content += f"""
            <div class='profile-card'>
                <h3>{member["name"]}</h3>
                <p><strong>{member["role"]}</strong></p>
                <p>{member["bio"]}</p>
            </div>
            """
        html_content += "</div>"  # Close the row div
    html_content += "</div>"  # Close the container div

    # Additional information section
    html_content = """
    <div class="info-section">
        <h3>Course: Intelligent Systems</h3>
        <p><strong>Instructor:</strong> Assoc. Prof. Quản Thành Thơ</p>
        <p><strong>Email:</strong> <a href="mailto:qttho@hcmut.edu.vn">qttho@hcmut.edu.vn</a></p>
        <h3>Project Contributors</h3>
    </div>
    """ + html_content

    html(html_content, height=1400)
