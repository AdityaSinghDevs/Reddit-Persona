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
    Use ONLY the provided content — do not invent details or make blind guesses
    - When a direct answer isn't available, provide your **best estimate** with a confidence label: HIGH / MEDIUM / LOW
    - For each inferred point, briefly explain your reasoning or context clues
    - Include **at least 3–5 direct Reddit quotes** across the persona to support your insights
    - If truly no data exists, first make an estimate and then clearly state: "Insufficient data"
        [e.g. Age: Estimated 25–35 (Insufficient direct evidence; inferred from vocabulary, subreddit usage, and cultural references — confidence: Medium)]
    - Ignore any other users mentioned or quoted in the content

    Generate the persona in this format:

    ----------------------------------
    Username : u/{username}
    DEMOGRAPHICS:
    - Age: [Best estimate + confidence level + reason or quote. Use explicit age only if found.]
    - Occupation: [Guessable from context, include confidence + explanation]
    - Location: [If inferred, mention how (e.g., language, subreddit, cultural reference)]
    - Tier: [e.g., Early Adopter, Passive Lurker, Community Contributor + rationale]
    - Archetype: [e.g., The Analyst, The Creator, The Explorer, etc.]

    Traits:
    - (3 to 5 adjectives describing this user's traits with 1-2 quotes if possible)

    Motivation (Ranked):
    1. [Primary motivation + reason + confidence]
    2. [Secondary motivation + reason]
    3. [Tertiary motivation + reason]
    (Use categories like curiosity, expression, connection, influence, growth etc.)


    Personality (MBTI style):
    • Introvert vs Extrovert: [...] 
    • Intuition vs Sensing: [...]
    • Thinking vs Feeling: [...]
    • Judging vs Perceiving: [...]
    • Likely Type: [e.g., INTP, ESTJ]
    For all give (Confidence + reason)

    Behaviour and Habits:
    - Bullet points Describing user's observed activity style, language, tone, subreddit choices, timing, etc.
    - Support 1-2 of these points with direct Reddit quotes if possible
    • Quote 1: "..."  
    • Quote 2: "..."

    Frustration:
    - Bullet points summarising what annoys, concerns, or irritates the user + 1–2 quotes if possible
    - User direct quotes of relevant

    Goals and Needs:
    - Bullet points stating what this user seems to care about, desire, aim to improve or seeks from Reddit

    QUOTE THAT CAPTURES ESSENCE
    "[[One quote that captures the user’s mindset, humor, or style]"

    Make sure the tone is professional and useful for product or UX designers to understand the user deeply
    IMPORTANT: ONLY generate the persona for the author of the provided posts/comments. 
    Ignore any other usernames that may be mentioned or quoted.
    
    --------------------------------                
    """

    full_persona_parts = []

    for i, chunk in enumerate(chunks):
        print(f"Sending Chunk {i+1}/{len(chunks)} to Groq...")

        user_prompt = (
            f"this is chunk{i+1} of Reddit activity from user u/{username}.\n"
            f"Generate a standalone persona from just this chunk.\n\n"
            f"Label the start of your output clearly as:\n"
            f"=== Persona based on Chunk {i+1} ===\n\n"
            f"{chunk}"
        )

        try:
            response = client.chat.completions.create(
                model  = model_name, 
                messages = [
                    {"role":"system", "content": sys_prompt.strip()},
                    {"role": "user", "content" : user_prompt.strip()}
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