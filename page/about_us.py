import streamlit as st
import base64

# Function to encode images to base64
def load_image(image_file):
    with open(image_file, "rb") as file:
        return base64.b64encode(file.read()).decode()

# Load images
journify_logo = load_image("Journify/resource/journify_logo.png")
hcmut_logo = load_image("Journify/resource/hcmut_logo.jpg")

# Define a function to display the "About Us" section
def display_about_us():
    # Team member data
    team_members = [
        {
            "name": "Huỳnh Thanh Tân",
            "role": "Machine Learning Developer",
            "id": "2392019",
            "email": "mailto:httan.sdh241@hcmut.edu.vn",
            "contribution": "Developed advanced NLP algorithms to enhance recommendation precision for the Intelligent Article Explorer."
        },
        {
            "name": "Trần Quốc Thái",
            "role": "Data Developer",
            "id": "2370759",
            "email": "mailto:tqthai.sdh232@hcmut.edu.vn",
            "contribution": "Engineered scalable data infrastructure, ensuring reliable performance and seamless data processing."
        },
        {
            "name": "Trần Vũ Hồng Thiên",
            "role": "Machine Learning Developer",
            "id": "2370303",
            "email": "mailto:tvhthien.sdh231@hcmut.edu.vn",
            "contribution": "Designed and optimized ML models, improving the efficiency and accuracy of recommendation features."
        },
        {
            "name": "Rehman Ibtasam",
            "role": "Data Developer",
            "id": "2370300",
            "email": "mailto:ribtasam.sdh231@hcmut.edu.vn",
            "contribution": "Developed user-friendly interfaces, providing a seamless experience for data visualization and exploration."
        }
    ]

    # CSS and HTML for team member cards
    html_content = f"""
    <style>
        body {{
            background-color: #ffffff;  
            font-family: Arial, sans-serif;
        }}
        .container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            padding: 20px;
        }}
        .row {{
            display: flex;
            gap: 30px;
            justify-content: center;
            width: 100%;
            flex-wrap: wrap;
        }}
        .profile-card {{
            background: #ffffff;  
            border-radius: 15px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            width: 280px;
            padding: 20px;
            text-align: center;
            position: relative;
            border: 2px solid transparent;
        }}
        .profile-card:hover {{
            box-shadow: 0 15px 25px rgba(0, 0, 0, 0.3);
            transform: translateY(-5px);
            border-color: #3498db;
        }}
        .profile-card::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 50%;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(52, 152, 219, 0.1), rgba(52, 152, 219, 0.05));
            z-index: 0;
            transition: transform 0.3s ease;
            border-radius: 15px;
            transform: translateX(-50%);
        }}
        .profile-card h3 {{
            margin: 10px 0;
            font-size: 1.5em;
            color: #333;
            position: relative;
            z-index: 1;
        }}
        .profile-card p {{
            color: #555;
            font-size: 1em;
            margin: 5px 0;
            line-height: 1.5em;
            position: relative;
            z-index: 1;
        }}
        .profile-card .contact-info {{
            margin-top: 10px;
            font-size: 0.9em;
        }}
        .contact-info a {{
            color: #3498db;
            text-decoration: none;
            position: relative;
            z-index: 1;
            transition: color 0.3s ease;
        }}
        .contact-info a:hover {{
            color: #2980b9;
            text-decoration: underline;
        }}
        .info-section {{
            text-align: center;
            font-family: Arial, sans-serif;
            margin-top: 20px;
        }}
        .info-section h3 {{
            font-size: 1.8em;
            margin-bottom: 5px;
        }}
        .info-section p {{
            font-size: 1em;
            color: #555;
        }}
    </style>
    
    <div class="info-section">
        <h3>About Journify</h3>
        <div style="display: flex; justify-content: center; gap: 50px; margin: 20px 0;">
            <img src="data:image/png;base64,{journify_logo}" alt="Intelligent Article Explorer Logo" width="150">
            <img src="data:image/jpeg;base64,{hcmut_logo}" alt="Bach Khoa University Logo" width="200">
        </div>
        <p><strong>Course:</strong> Intelligent Systems</p>
        <p><strong>Instructor:</strong> Assoc. Prof. Quản Thành Thơ</p>
        <p><strong>Email:</strong> <a href="mailto:qttho@hcmut.edu.vn">qttho@hcmut.edu.vn</a></p>
        <h3>Project Contributors</h3>
    </div>
    
    <div class='container'>
    """

    # Generate HTML for each team member in two-member rows
    for i in range(0, len(team_members), 2):
        html_content += "<div class='row'>"
        for member in team_members[i:i+2]:
            html_content += f"""
            <div class='profile-card'>
                <h3>{member["name"]}</h3>
                <p><strong>ID:</strong> {member["id"]}</p>
                <p><strong>{member["role"]}</strong></p>
                <p>{member["contribution"]}</p>
                <div class="contact-info">
                    <p><strong>Email:</strong> <a href="{member["email"]}">{member["email"].replace("mailto:", "")}</a></p>
                </div>
            </div>
            """
        html_content += "</div>"  # Close the row div
    html_content += "</div>"  # Close the container div
    
    # Footer
    html_content += """
    <div class="info-section">
        <h3>Source Code & Support</h3>
        <p><a href="#">GitHub Repository</a> | <a href="#">Support Us</a></p>
    </div>
    <hr>
    <p style="text-align: center; color: #555;">© 2024 Intelligent Article Explorer. All rights reserved.</p>
    """
    
    st.components.v1.html(html_content, height=1200)

if __name__ == "__main__":
    display_about_us()
