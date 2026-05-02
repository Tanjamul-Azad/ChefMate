

from flask import Flask, render_template, request
from predict import predict_recipes

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        ingredients = request.form.get("ingredients", "")
        ingredients = ingredients.replace(", ", ",").strip()
        user_ingredients = [i.strip().replace(" ", "_") for i in ingredients.split(",") if i.strip()]
        cuisine = request.form.get("cuisine") or None
        diet = request.form.get("diet") or None
        meal_type = request.form.get("meal_type") or None
        results = predict_recipes(
            user_ingredients,
            cuisine=cuisine,
            diet=diet,
            meal_type=meal_type
)
        return render_template("result.html", results=results)

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
