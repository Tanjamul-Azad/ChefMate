

import pandas as pd
from utils import normalize_ingredient

def preprocess_data(input_csv='recipes.csv', output_csv='cleaned_recipes.csv'):
    df = pd.read_csv(input_csv)

    def clean_ings(ings):
        if not isinstance(ings, str):
            return ""
        return " ".join([normalize_ingredient(i.strip()) for i in ings.split(',')])
    df['Cuisine'] = df['Cuisine'].astype(str).str.strip().str.lower()
    df['Diet'] = df['Diet'].astype(str).str.strip().str.lower()
    df['Meal Type'] = df['Meal Type'].astype(str).str.strip().str.lower()

    df['Cleaned_Ingredients'] = df['Ingredients'].apply(clean_ings)
    df.to_csv(output_csv, index=False)
    print("✅ Data cleaned and saved to", output_csv)

if __name__ == "__main__":
    preprocess_data()
