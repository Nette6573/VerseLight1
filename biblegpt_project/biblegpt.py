import os
import pandas as pd
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Retrieve the API key from the environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Make sure the API key is being read correctly
if not GOOGLE_API_KEY:
    raise ValueError("Google API Key is not set. Please check your .env file.")

# Configure the Gemini API key
genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini model
model = genai.GenerativeModel("gemini-pro")

# Load Bible dataset (assuming the 'bible_data_set.csv' file exists)
bible_df = pd.read_csv('bible_data_set.csv')

# JSON file to save generated verses
SAVED_VERSES_FILE = 'saved_verses.json'

# Save verse to a JSON file
def save_verse(verse):
    if os.path.exists(SAVED_VERSES_FILE):
        with open(SAVED_VERSES_FILE, 'r') as f:
            saved_verses = json.load(f)
    else:
        saved_verses = []

    saved_verses.append(verse)

    with open(SAVED_VERSES_FILE, 'w') as f:
        json.dump(saved_verses, f, indent=4)

# Get a random Bible verse from CSV
def get_random_verse():
    verse = bible_df.sample(1).iloc[0]
    return f"{verse['citation']} - {verse['text']}"

# Search the CSV for a verse by keyword
def search_verse(keyword):
    results = bible_df[bible_df['text'].str.contains(keyword, case=False, na=False)]
    if results.empty:
        return "No verses found with that keyword."
    verse = results.sample(1).iloc[0]
    return f"{verse['citation']} - {verse['text']}"

# Generate a custom Bible-style verse with Gemini
def generate_bible_style_verse(prompt):
    full_prompt = f"Write a poetic Bible-style verse in King James English about: {prompt}"

    try:
        # Call Gemini to generate the verse based on the prompt
        response = model.generate_content(full_prompt)
        verse = response.text.strip()

        # Save the generated verse to a file
        save_verse(verse)

        return verse
    except Exception as e:
        return f"Error generating verse: {str(e)}"
