from flask import Flask, render_template, request
from utils import load_recipes, match_recipes

app = Flask(__name__)
df = load_recipes()

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        ingredients = request.form.get("ingredients", "")
        user_ingredients = [i.strip() for i in ingredients.split(",") if i.strip()]

        cuisine = request.form.get("cuisine") or None
        diet = request.form.get("diet") or None
        meal_type = request.form.get("meal_type") or None

        # ✅ FIXED here
        matched = match_recipes(
            user_ingredients,
            df,
            cuisine=cuisine,
            diet=diet,
            meal_type=meal_type
        )
        return render_template("result.html", results=matched)

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
