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
    

main()