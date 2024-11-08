import praw

# Configure your Reddit API credentials
reddit = praw.Reddit(
    client_id="XXYeobSbUIHWVCHYBUxAcA",
    client_secret="xcblb9gcJ13ZmWF7o9UrwGZRDws6Bg",
    user_agent="MyRedditBot/0.1 by YourUsername",
    password="Tan0128631!!!",
    username="tanht1997",
)

# Search for discussions about the arXiv paper
search_query = "The arXiv paper: Attention is All you Need"
for submission in reddit.subreddit("all").search(search_query, limit=2):
    print("Title:", submission.title)
    print("URL:", submission.url)
    print("Comments:")

    # Fetch and print comments from each post
    submission.comments.replace_more(limit=0)  # Load all comments
    for comment in submission.comments.list():
        print(" -", comment.body)


# import requests

# def get_citation_count(arxiv_id):
#     # Construct the Semantic Scholar API URL
#     url = f'https://api.semanticscholar.org/v1/paper/arXiv:{arxiv_id}'

#     # Send a GET request to the API
#     response = requests.get(url)
#     # Check if the request was successful
#     if response.status_code == 200:
#         data = response.json()
#         citation_count = data.get('influentialCitationCount', 0)
#         return citation_count
#     else:
#         print(f"Error: Unable to fetch data (Status code: {response.status_code})")
#         return None

# # Example usage
# # arxiv_id = '0704.0001'
# arxiv_id = '1706.03762'
# citation_count = get_citation_count(arxiv_id)
# if citation_count is not None:
#     print(f"The paper with arXiv ID {arxiv_id} has been cited {citation_count} times.")
