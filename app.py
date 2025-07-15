import streamlit as st
from scraper import init_reddit_client, scrape_user_data
from llm_inferencer import chunk_user_data, generate_persona_from_text, evaluate_and_append_best_persona
from formatter import format_persona_output, save_persona_to_txt
from main import get_username_from_url
import os

st.set_page_config(page_title="Reddit Persona Generator", layout="centered")

st.title("Reddit Persona Generator")

st.markdown(
    """
This tool analyzes a Reddit user's public activity (posts and comments) to generate a detailed persona using Groq's LLaMA-3.3 70B model.
"""
)

# Input field
input_url = st.text_input("Enter Reddit Username or Profile URL (e.g. https://www.reddit.com/user/username/)")

# Checkbox to optionally evaluate best persona
enable_eval = st.checkbox("Evaluate and append best persona chunk (experimental)")

# Button to trigger persona generation
if st.button("Generate Persona") and input_url:
    username = get_username_from_url(input_url)

    if not username:
        st.error("Invalid Reddit profile URL or username.")
    else:
        st.info(f"Fetching data for user: u/{username}...")

        with st.spinner("Initializing Reddit client and scraping user data..."):
            reddit = init_reddit_client()
            user_texts = scrape_user_data(reddit, username)

        if not user_texts:
            st.warning("No valid posts or comments found for this user.")
        else:
            st.success("Reddit data successfully scraped.")

            with st.spinner("Chunking text and sending data to LLM..."):
                chunks = chunk_user_data(user_texts)
                persona_dict = generate_persona_from_text(chunks, username=username)

            raw_persona = persona_dict["persona_raw"]
            formatted_output = format_persona_output(raw_persona)

            # Save to file
            save_persona_to_txt(username, formatted_output)

            # Optional Evaluation
            if enable_eval:
                with st.spinner("Evaluating and appending best persona chunk..."):
                    evaluate_and_append_best_persona(
                        filepath=f"sample_outputs/{username}_persona.txt",
                        username=username
                    )

            st.success(f"Persona for u/{username} generated successfully.")
            st.markdown("### Final Persona Output")
            st.text_area("Generated Persona", value=formatted_output, height=700)

            with st.expander("View Raw Persona (Unformatted)"):
                st.text_area("Raw Persona Output", value=raw_persona, height=700)

            output_path = os.path.join("sample_outputs", f"{username}_persona.txt")
            if os.path.exists(output_path):
                with open(output_path, "r", encoding="utf-8") as f:
                    content = f.read()
                st.download_button(
                    label="Download Persona as .txt",
                    data=content,
                    file_name=f"{username}_persona.txt",
                    mime="text/plain"
                )
