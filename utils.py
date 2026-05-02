# utils.py
from rapidfuzz import process

import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")

INGREDIENT_SYNONYMS = {
    "chili": "chili pepper",
    "bell pepper": "capsicum",
    "garbanzo bean": "chickpea",
    "courgette": "zucchini",
    "aubergine": "eggplant",
    "scallion": "green onion"
}
def fuzzy_correct(ingredient, known_ingredients, threshold=80):
    match, score, _ = process.extractOne(ingredient, known_ingredients)
    if score >= threshold:
        return match
    return ingredient  

def normalize_ingredient(text, known_ingredients=None):
    text = text.lower().replace("_", " ")  
    doc = nlp(text)
    lemma = " ".join([token.lemma_ for token in doc if token.is_alpha])
    lemma = INGREDIENT_SYNONYMS.get(lemma, lemma.replace(" ", "_"))  

    
    if known_ingredients:
        return fuzzy_correct(lemma, known_ingredients)
    return lemma

def load_recipes(file_path='recipes.csv'):
    df = pd.read_csv(file_path)

    # ✅ Remove duplicate recipes based on name (to avoid repeated results)
    df = df.drop_duplicates(subset=["Recipe Name"])

    return df

