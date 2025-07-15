from config import reddit_client_id, reddit_client_secret, reddit_user_agent
import praw
from datetime import datetime


# print(f"Client ID: {reddit_client_id}")
# print(f"Client Secret: {reddit_client_secret[:10]}...")  # Only first 10 chars
# print(f"User Agent: {reddit_user_agent}") 
#Testing the keys

def init_reddit_client():
    """Initialize the Reddit client. in Read-only instance using PRAW
    
    Returns : praw.Reddit -> Configured Reddit instance for API access"""
    reddit = praw.Reddit(client_id = reddit_client_id,
                     client_secret = reddit_client_secret,
                        user_agent = reddit_user_agent)
    return reddit 

def scrape_user_data(reddit, username, max_comments=30, max_posts = 10):
    """ This function will scrape the user data from reddit.
    
    Args:
       - reddit (praw.Reddit): Initialized Reddit client.
       - username (str) : Reddit username to scrape data from
       - max_comments(int)[optional]: Maximum number of comments to fetch, Dedault set to 30
       - max_posts(int)[optional]: Maximum number of posts to fetch, Dedault set to 10

    Returns:
        user_texts (list): List of timestamped strings containing user comments and post content

    [Note]:
        Skips '[deleted]' content and handles exceptions with error logging
    """
    
    #User Profile
    user = reddit.redditor(username)
    user_texts = []

    #Getting comments
    try:
        for comment in user.comments.new(limit=max_comments):
            if comment.body and comment.body.strip().lower() != '[deleted]':
                ts = datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d')
                formatted = f"[Comment on {ts}]\n{comment.body.strip()}"
                user_texts.append(formatted.strip())
                
    except Exception as e:
        print(f"[!!!]Error Fetching comments for {username} : {e}")

    #Getting posts or submissions (in reddit terms)
    try :
        for submission in user.submissions.new(limit=max_posts) :
              if submission.title or submission.selftext:
                ts = datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d')
                text = submission.title or ""
                if submission.selftext:
                    text += "\n" + submission.selftext.strip()
                text = text.strip()
                if text and text.lower() != '[deleted]':
                    formatted = f"[Post on {ts}]\n{text}"
                    user_texts.append(formatted)
    except Exception as e:
        print(f"[!!!]Error fetching post for {username} : {e}")

    return user_texts
