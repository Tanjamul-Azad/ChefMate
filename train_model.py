# train_model.py

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
import pickle

def train_model(csv_file='cleaned_recipes.csv', model_file='model.pkl'):
    df = pd.read_csv(csv_file)

    # 🔥 Drop duplicates BEFORE training
    df = df.drop_duplicates(subset='Recipe Name').reset_index(drop=True)

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['Cleaned_Ingredients'])

    model = NearestNeighbors(metric='cosine', algorithm='brute')
    model.fit(X)

    with open(model_file, 'wb') as f:
        pickle.dump((model, vectorizer, df), f)

    print("✅ Model trained and saved to", model_file)

if __name__ == "__main__":
    train_model()


