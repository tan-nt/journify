import requests

def get_citation_count(arxiv_id):
    # Construct the Semantic Scholar API URL
    url = f'https://api.semanticscholar.org/v1/paper/arXiv:{arxiv_id}'

    # Send a GET request to the API
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        citation_count = data.get('influentialCitationCount', 0)
        return citation_count
    else:
        print(f"Error: Unable to fetch data (Status code: {response.status_code})")
        return None

# Example usage
# arxiv_id = '0704.0001'
arxiv_id = '1706.03762'
citation_count = get_citation_count(arxiv_id)
if citation_count is not None:
    print(f"The paper with arXiv ID {arxiv_id} has been cited {citation_count} times.")
