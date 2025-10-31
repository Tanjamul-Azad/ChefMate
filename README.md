# 🍳 ChefMate — Your Smart AI Recipe Assistant  

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Framework-lightgrey?logo=flask)
![spaCy](https://img.shields.io/badge/spaCy-NLP-green?logo=spacy)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success)
![Platform](https://img.shields.io/badge/Platform-Web-orange)

---

**ChefMate** is an AI-powered recipe web application built with **Flask**, designed to help users discover the perfect dish from whatever ingredients they have at home.  
It combines **NLP (spaCy)**, **fuzzy matching**, and **machine learning** to normalize ingredients, predict cuisines, and even suggest recipe names — all wrapped in a beautiful, user-friendly interface.

---

## 🚀 Features  

### 🧠 AI & NLP Intelligence  
- **Ingredient Normalization:** Uses **spaCy** lemmatization and synonym handling to understand ingredient variations (e.g., *“tomatoes” → “tomato”*).  
- **Fuzzy Matching:** Smartly matches ingredients even with typos or variations.  
- **Ingredient Categorization (Planned):** Classify ingredients by type (spices, dairy, etc.) for smarter suggestions.  

### 🤖 Machine Learning Predictions  
- Predict **recipe names** and **cuisines** from ingredient lists using a Kaggle dataset (~643 MB).  
- The ML model learns flavor patterns and relationships between cuisines.  

### 💡 Smart User Experience  
Clean and responsive Flask frontend.  

Dropdown filters for:  
- 🥗 **Cuisine**  
- 🥦 **Diet type**  
- 🍛 **Meal type**  

Fast recipe results with a matching score display.  

### 🔮 Upcoming “Later Upgrades”  
- 🔍 Search bar with live filtering  
- 🌎 Filter by cuisine & difficulty  
- ❤️ Save favorite recipes  
- ⭐ Add ratings and comments  
- 🛒 Export smart shopping list  

---

## 🏗️ Tech Stack  

| Category | Technology |
|-----------|-------------|
| **Backend** | Flask (Python) |
| **Frontend** | HTML5, CSS3, JavaScript |
| **AI/NLP** | spaCy, FuzzyWuzzy |
| **ML (Future)** | Scikit-learn, Pandas, NumPy |
| **Dataset** | Kaggle recipe dataset (ingredients, steps, tags) |
| **Environment** | Virtualenv / Conda |

---

## ⚙️ Installation & Setup  

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/ChefMate.git
   cd ChefMate
2. Create & activate virtual environment

python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows


3. Install dependencies

pip install -r requirements.txt


4. Run the Flask app

python app.py


5. Visit locally

http://127.0.0.1:5000/

🧩 Project Structure
ChefMate/
│
├── app.py                 # Main Flask app
├── utils.py               # NLP + Matching utilities
├── static/                # CSS, JS, images
├── templates/             # HTML templates
├── models/                # ML model files (planned)
├── data/                  # Dataset files
├── requirements.txt
└── README.md

🧠 How It Works

User enters ingredients.

spaCy normalizes input (lemmatization + synonym handling).

Fuzzy matching compares against the dataset ingredients.

Matching recipes are displayed with confidence scores.

(Future) The ML model predicts likely cuisine and recipe name.
