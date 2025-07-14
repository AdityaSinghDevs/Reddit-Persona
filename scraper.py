from config import reddit_client_id, reddit_client_secret, reddit_user_agent, groq_api_key
import praw


# print(f"Client ID: {reddit_client_id}")
# print(f"Client Secret: {reddit_client_secret[:10]}...")  # Only first 10 chars
# print(f"User Agent: {reddit_user_agent}") 
#Testing the keys

def init_reddit_client():
    """Initialize the Reddit client. in Read-only instance"""
    reddit = praw.Reddit(client_id = reddit_client_id,
                     client_secret = reddit_client_secret,
                        user_agent = reddit_user_agent)
    return reddit 

def scrape_user_data(reddit, username, max_comments=30, max_posts = 10):
    """ This function will scrape the user data from reddit."""
    
    #User Profile
    user = reddit.redditor(username)
    user_texts = []

    #Getting comments
    try:
        for comment in user.comments.new(limit=max_comments):
            if comment.body and comment.body.strip().lower() != '[deleted]':
                user_texts.append(comment.body.strip())
    except Exception as e:
        print(f"[!]Error Fetching comments for {username} : {e}")

    #Getting posts or submissions in reddit terms
    try :
        for submission in user.submissions.new(limit=max_posts) :
            text = submission.title or ""
            if submission.selftext:
                text += "\n" + submission.selftext
                text = text.strip()
                if text and text.lower() != '[deleted]':
                    user_texts.append(text)   
    except Exception as e:
        print(f"[!]Error fetching post for {username} : {e}")

    return user_texts
