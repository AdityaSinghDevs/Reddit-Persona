from scraper import init_reddit_client, scrape_user_data

def get_username_from_url(url):
    '''This function extracts username from url provided'''
    parts = url.strip().rstrip("/")

    if "/" not in url and not url.startswith("http"):
        return url #In case the username is directly provided

    parts = [p for p in url.split("/") if p]

    for i in  range(len(parts) - 1):
        if parts[i] in ("user","u"):
            return parts[i +1]
    return None 
#Trailing slashes, username and 'u' handled here

def main():
    print("Reddit Persona Gen\n")

    url  = input("Enter url for the Reddit Profile : ")
    username  = get_username_from_url(url)

    if not username :
        print( "[!]Invalid Profile or URL format.[!]")
        return
    
    print(f"Fetching data for user : u/{username}...")

    reddit  = init_reddit_client()
    user_texts = scrape_user_data(reddit, username)  

    
    # with open(f"{username}_data.txt", "w", encoding="utf-8") as f:
    #     f.write(f"Reddit data for user: {username}\n")
    #     f.write("="*50 + "\n\n")
    #     for i, text in enumerate(user_texts, 1):
    #         f.write(f"--- Item {i} ---\n")
    #         f.write(f"{text}\n\n")
    
    # print(f"Data saved to {username}_data.txt")
    #Checking what the output feels like 

main()