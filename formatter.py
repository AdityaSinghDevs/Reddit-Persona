import os 

def format_persona_output(raw_text:str)-> str:
    '''
    Cleans and formats raw persona output from the LLM
    Removes any duplicacy, extra spaces, and normalize section breaks
    
    Args:
        raw_text (str) : Raw persona text from the LLM.

    Returns:
        (str) : Formatted persona text    
    
    '''

    lines = raw_text.strip().splitlines()
    seen = set()
    formatted_lines = []

    for line in lines:
        clean_line = line.strip()

        #avoiding blank line stacking
        if clean_line == "" and (not formatted_lines or formatted_lines[-1]==""):
            continue

        #Remove exact duplicate lines (except blank ones)
        if clean_line and clean_line not in seen:
            formatted_lines.append(clean_line)
            seen.add(clean_line)
        elif clean_line == "":
            formatted_lines.append("")

    return "\n".join(formatted_lines).strip()

def save_persona_to_txt(username:str, cleaned_text:str):  
    '''Saving cleaned persona output into sample_outputs directory as <username>_persona.txt

    Args:
        username (str) : Reddit username for file naming
        cleaned_text (str) : Formatted persona text to save 
    '''

    os.makedirs("sample_outputs", exist_ok=True)
    filepath = os.path.join("sample_outputs", f"{username}_persona.txt")

    with open(filepath, "w", encoding = "utf-8") as f:
        f.write(cleaned_text)

    print(f"FORMATTED PERSONA SUCCESSFULLY SAVED AT : {filepath}")    