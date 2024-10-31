import requests
from bs4 import BeautifulSoup

def get_arxiv_category_mapping():
    url = "https://arxiv.org/category_taxonomy"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print('soup:', soup)

    category_mapping = {}

    # Find all category elements on the page
    for category in soup.find_all("span", class_="category-name"):
        abbreviation = category.find("code").text.strip()  # Category abbreviation
        full_name = category.find("strong").text.strip()   # Full name
        category_mapping[abbreviation] = full_name

    return category_mapping

# Fetch the mapping
category_mapping = get_arxiv_category_mapping()
print(category_mapping)  # Print or save the dictionary as needed
