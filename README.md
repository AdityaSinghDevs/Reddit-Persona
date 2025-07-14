# Reddit-Persona
This repository contains a Reddit profile scraper that builds user personas from posts and comments, using LLMs for analysis and summarization.

# PRAW
Reddit Account:
A Reddit account is required to access Reddit’s API. Create one at reddit.com.

Client ID & Client Secret:
These two values are needed to access Reddit’s API as a script application (see Authenticating via OAuth for other application types). If you don’t already have a client ID and client secret, follow Reddit’s First Steps Guide to create them.

User Agent:
A user agent is a unique identifier that helps Reddit determine the source of network requests. To use Reddit’s API, you need a unique and descriptive user agent. The recommended format is <platform>:<app ID>:<version string> (by u/<Reddit username>). For example, android:com.example.myredditapp:v1.2.3 (by u/kemitche). Read more about user agents at Reddit’s API wiki page.