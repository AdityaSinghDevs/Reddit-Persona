from config import groq_api_key
from groq import Groq

model_name = "llama-3.3-70b-versatile" #Can modify the model being used form here

'''Groq's API SDK'''
client = Groq(api_key = groq_api_key)
# chat_completion = client.chat.completions.create(
#     messages=[
#         # Set an optional system message. This sets the behavior of the
#         # assistant and can be used to provide specific instructions for
#         # how it should behave throughout the conversation.
#         {
#             "role": "system",
#             "content": "You are a helpful assistant."
#         },
#         # Set a user message for the assistant to respond to.
#         {
#             "role": "user",
#             "content": "Explain the importance of fast language models",
#         }
#     ],

#     # The language model which will generate the completion.
#     model=model_name
# )

# # Print the completion returned by the LLM.
# print(chat_completion.choices[0].message.content)

def chunk_user_data(text_list, max_chars=2000):
    '''
    Splitting Reddit user text into smaller chunks for LLM input
    '''

    if not text_list:
        return []
    
    if max_chars < 1:
        #handling negative edge case for max_char input
        raise ValueError("max_chars must be positive") 

    chunks = []
    current_chunk = ""

    for text in text_list:

        if not text.strip():
            continue 

        if len(current_chunk) + len(text) <= max_chars:
            current_chunk += text + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = text + "\n\n"
            
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def generate_persona_from_text(chunks, username ="UnknownUser", model=model_name):
    '''
    Sends Reddit text chunks to Groq's LLM and builds a structured user persona'''

    sys_prompt = f"""
    You are an expert UX researcher and behavioral analyst specializing in creating detailed user personas from digital footprints.
     
    Your task is to analyze Reddit posts and comments from user u/{username} and create a comprehensive and complete user persona tailored for product and UX teams. inspired by UX user research documentation formats.The output must be structured, readable, and insightful.

    Analysis Guidelines:
    - Use ONLY the provided content — no assumptions
    - Clearly distinguish between direct evidence and educated guesses
    - When making inferences, mark your confidence as HIGH / MEDIUM / LOW
    - Include direct quotes for important traits (at least 3–5 in total)
    - If there's not enough info, write "Insufficient data" — do not guess
    - Ignore any other users mentioned or quoted in the text
        
    Generate the persona in this format:

    ----------------------------------
    Username : u/{username}
    Data Source: 
    Estimated Age: (make the most accurate guess as possible or if you find age somewhere in the text, use that)
    Occupation: (guessable from context)
    Location : (Guess if inferred)
    Tier : (e.g., Early Adopter, Passive Lurker, Community Contributor)
    Archetype: (e.g. The Analyst, The Creator, The Explorer)

    Traits:
    - (3 to 5 adjectives describing this user's traits)

    Motivation:
    - (Ranked list of Motivations : curiosity, expression, connection, etc.)

    Personality (MBTI style):
    - Introvert vs Extrovert: (guess)
    - Intuition vs Sensing: (guess)
    - Thinking vs Feeling: (guess)
    - Judging vs Perceiving: (guess)
    - Personality type : (using the collective of above)

    Behaviour and Habits:
    - Bullet points Describing user's observed activity style, language, tone, subreddit choices, timing, etc.
    - Support 1-2 of these points with direct Reddit quotes if possible

    Frustration:
    - Bullet points summarising what annoys, concerns, or irritstes the user
    - User direct quotes of relevant

    Goals and Needs:
    - Bullet points stating what this user seems to care about, desire or aim to improve

    Make sure the tone is professional and useful for product or UX designers to understand the user deeply
    IMPORTANT: ONLY generate the persona for the author of the provided posts/comments. 
    Ignore any other usernames that may be mentioned or quoted.
    
    --------------------------------                
    """

    full_persona_parts = []

    for i, chunk in enumerate(chunks):
        print(f"Sending Chunk {i+1}/{len(chunks)} to Groq...")

        try:
            response = client.chat.completions.create(
                model  = model_name, 
                messages = [
                    {"role":"system", "content": sys_prompt.strip()},
                    {"role": "user", "content" : chunk.strip()}
                ]
            )

            persona_piece = response.choices[0].message.content
            full_persona_parts.append(persona_piece)

        except Exception as e:
            print(f"[!] LLM error on chunk : {i+1} : {e}")
    

    full_persona = "\n\n".join(full_persona_parts)

    return {
        "username":username,
        "persona_raw": full_persona
    }