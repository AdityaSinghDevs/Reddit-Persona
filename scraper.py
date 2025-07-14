from config import reddit_client_id, reddit_client_secret, reddit_user_agent, groq_api_key
import praw


def init_reddit_client():
    """Initialize the Reddit client."""
    reddit = praw.Reddit(client_id = reddit_client_id,
                     client_secret = reddit_client_secret,
                        user_agent = reddit_user_agent)
    return reddit 

def scrape_user_data(reddit, username, max_comments=30, max_posts = 10):
    """ This funnction will scrape the user data from reddit."""
    
#Profile
profile = reddit.redditor('kojied')
