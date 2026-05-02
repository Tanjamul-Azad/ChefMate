import pickle
from utils import normalize_ingredient

def load_model(model_file='model.pkl'):
    with open(model_file, 'rb') as f:
        model, vectorizer, df = pickle.load(f)
    return model, vectorizer, df

def predict_recipes(user_ingredients, cuisine=None, diet=None, meal_type=None, top_k=None):

    model, vectorizer, df = load_model()
    filtered_df = df.copy()

    print("\n--- FILTER DEBUG ---")
    print(f"User Ingredients: {user_ingredients}")
    print(f"Selected Cuisine: {cuisine}")
    print(f"Selected Diet: {diet}")
    print(f"Selected Meal Type: {meal_type}")
    print(f"Total Recipes Loaded: {len(df)}")


    def safe_match(col, target):
        return col.fillna("").str.strip().str.lower() == target.strip().lower()

    print("[DEBUG] Total recipes before filtering:", len(df))

    if cuisine:
        print(f"[Cuisine Filter] Looking for: '{cuisine.strip().lower()}'")
        print("[Cuisine Column Unique Values]:", filtered_df['Cuisine'].dropna().unique())
        filtered_df = filtered_df[safe_match(filtered_df['Cuisine'], cuisine)]
        print(f"[Cuisine Filter] Recipes left: {len(filtered_df)}")

    if diet:
        filtered_df = filtered_df[safe_match(filtered_df['Diet'], diet)]
        print(f"[Diet Filter] Recipes left: {len(filtered_df)}")

    if meal_type:
        print(f"[Meal Type Filter] Looking for: '{meal_type.strip().lower()}'")
        print("[Meal Type Column Unique Values]:", filtered_df['Meal Type'].dropna().unique())
        filtered_df = filtered_df[safe_match(filtered_df['Meal Type'], meal_type)]
        print(f"[Meal Type Filter] Recipes left: {len(filtered_df)}")
   
   
    if filtered_df.empty:
        return [{
            'recipe': 'No recipes found',
            'matched': [],
            'missing': [],
            'score': 0,
            'suggestions': [],
            'instructions': 'No recipe available under the selected filters.',
            'cuisine': cuisine or 'Any',
            'diet': diet or 'Any',
            'meal_type': meal_type or 'Any',
            'ingredient_list': []
        }]
        
    filtered_df = filtered_df.drop_duplicates(subset='Recipe Name').reset_index(drop=True)
    print(f"[DEBUG] Filtered recipes after removing duplicates: {len(filtered_df)}")

    
    X = vectorizer.transform(filtered_df['Cleaned_Ingredients'])

    
    known_ingredients = set()
    for ing in df['Cleaned_Ingredients']:
        if isinstance(ing, str):
            known_ingredients.update(ing.split())

   
    cleaned_input = [
        normalize_ingredient(i, known_ingredients)
        for i in user_ingredients
    ]

    query = " ".join(cleaned_input)
    query_vec = vectorizer.transform([query])

    n = len(filtered_df)
    if top_k is None or top_k > n:
        top_k = n 
    distances, indices = model.kneighbors(query_vec, n_neighbors=top_k)

    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if idx >= len(filtered_df):
            continue

        row = filtered_df.iloc[idx]
        recipe_ingredients = row['Cleaned_Ingredients'].split()

        matched = set(cleaned_input) & set(recipe_ingredients)
        missing = set(recipe_ingredients) - set(cleaned_input)
        print(f"[DEBUG] Cleaned user input: {cleaned_input}")
        print(f"[DEBUG] Recipe ingredients: {recipe_ingredients}")
        print(f"[DEBUG] Matched: {matched}")
        print("\n--- MATCH DEBUG ---")
        print(f"Cleaned User Ingredients: {cleaned_input}")
        print(f"Recipe Ingredients: {recipe_ingredients}")
        print(f"Matched: {matched}")
        print(f"Missing: {missing}")

        if cleaned_input and len(matched) == 0:
            continue

        score = round((len(matched) / len(recipe_ingredients)) * 100)

        raw_ingredients = row.get('Ingredients', '').split(',')
        raw_quantities = row.get('Quantity', '').split(',')

        quantity_map = {}
        for ing, qty in zip(raw_ingredients, raw_quantities):
            if not isinstance(ing, str) or not isinstance(qty, str):
                continue
            norm_ing = normalize_ingredient(ing.strip())
            quantity_map[norm_ing] = qty.strip()

        suggestions = [
            f"{item} (Buy or borrow {quantity_map.get(item, 'some')})"
            for item in missing
        ]

        results.append({
            'recipe': row['Recipe Name'],
            'matched': list(matched),
            'missing': list(missing),
            'score': score,
            'suggestions': suggestions,
            'instructions': row.get('Instructions', 'No instructions provided'),
            'cuisine': row.get('Cuisine', 'Unknown'),
            'diet': row.get('Diet', 'Unknown'),
            'meal_type': row.get('Meal Type', 'Unknown'),
            'ingredient_list': [
                quantity_map.get(ing, ing)
                for ing in recipe_ingredients
            ]
        })

   
    if not results:
        return [{
            'recipe': 'No matching recipes',
            'matched': [],
            'missing': [],
            'score': 0,
            'suggestions': [],
            'instructions': 'No recipe matches the given ingredients in the selected category.',
            'cuisine': cuisine or 'Any',
            'diet': diet or 'Any',
            'meal_type': meal_type or 'Any',
            'ingredient_list': []
        }]
    print(f"[After All Filters] Total recipes to compare: {len(filtered_df)}")

    return sorted(results, key=lambda x: x['score'], reverse=True)

