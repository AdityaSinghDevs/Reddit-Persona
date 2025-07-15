from scraper import init_reddit_client, scrape_user_data
from formatter import format_persona_output, save_persona_to_txt
from llm_inferencer import chunk_user_data, generate_persona_from_text, evaluate_and_append_best_persona

def get_username_from_url(url):
    '''This function extracts username from url provided
    
    Handles trailing slashes, 'user', and 'u' segments.

    Args:
        url (str): Reddit profile URL or username.

    Returns:
        str or None : Extracted username or None if invalid    
    '''
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
    '''
    Main function to generate as Reddit user persona.

    Prompts for a URL, scrapes data, generates a persona and saves it to a file
    '''

    print("Reddit Persona Gen\n")

    url  = input("Enter url for the Reddit Profile : ")
    username  = get_username_from_url(url)

    if not username :
        print( "[!!!]Invalid Profile or URL format.[!!!]")
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

    #Checking what the output looks like 

    chunks = chunk_user_data(user_texts)
    persona_dict = generate_persona_from_text(chunks, username=username)

    #Testing output of llm into text file
    # with open(f"{username}_persona_raw.txt", "w", encoding="utf-8") as f:
    #     f.write(persona_dict["persona_raw"])

    # print(f"\n Full raw persona saved to: {username}_persona_raw.txt\n")
    
    #Formatting the output LLM gave
    cleaned_data = format_persona_output(persona_dict["persona_raw"])

    #Saving it to a .txt file in sample_outputs/
    save_persona_to_txt(username, cleaned_data)

    evaluate_and_append_best_persona(filepath=f"sample_outputs/{username}_persona.txt", username=username)

if __name__ == "__main__":
    main()