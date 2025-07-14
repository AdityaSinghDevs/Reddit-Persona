import os
from dotenv import load_dotenv

groq_api_key = os.getenv("GROQ_API_KEY")
reddit_client_id = os.getenv("CLIENT_ID") 
reddit_client_secret = os.getenv("CLIENT_SECRET")
reddit_user_agent = os.getenv("USER_AGENT")
