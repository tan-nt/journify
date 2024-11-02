import requests

def get_citation_count(arxiv_id):
    """
    Fetches the citation count for a given arXiv paper using the Semantic Scholar API.

    Parameters:
    arxiv_id (str): The arXiv identifier of the paper (e.g., '0704.0001').

    Returns:
    int: The number of citations the paper has received.
    """
    try:
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
            # TODO: use None instead
            return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0