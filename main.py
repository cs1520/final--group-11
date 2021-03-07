from flask import Flask, render_template, request
from fuzzywuzzy import fuzz
# FLASK_APP=main.py FLASK_ENV=development flask run

app = Flask(__name__)


@app.route("/")
def home():
    """Return a simple HTML page."""
    print("Hit the route!")
    return render_template("index.html")

@app.route("/search")
def search():
    """Return a simple HTML page."""
    print("Search route!")
    return render_template("search.html", wings=[])


all_wings = [{"name": "Ace Boogie", "description": "Black Magic, Butter, Dry Ranch"},   
                {"name": "Ain't My Faulks", "description": "Butter, Dry BBQ, Dry Garlic, Dry Ranch"},
                {"name": "B.A.D.", "description": "Buttered Atomic Dust"}]

@app.route("/search-results/", methods=["POST"])
def search_results():
    """Return a simple HTML page."""
    print("Searching!")
    test_wings = []
    s_term = request.form['searchterm']
    s_term = s_term.split(',')
    print(s_term)
    #comp_term = "Ain't My Faulks"

    for w in all_wings:
        name_PR = 0
        des_PR = 0
        tot_des_PR = 0
        if len(s_term) == 1:    
            name_PR = fuzz.partial_ratio(s_term[0].lower(),w["name"].lower())

        for s in range(len(s_term)):
            des_PR = fuzz.partial_ratio(s_term[s].lower(),w["description"].lower())
            tot_des_PR = tot_des_PR + des_PR

        tot_des_PR = tot_des_PR/(len(s_term))
        print(tot_des_PR)
        if name_PR > 65 or tot_des_PR > 65:
            #print("passed!")
            #print(w["name"])
            test_wings.append(w)

    return render_template("search.html", wings=test_wings)

@app.route("/profile")
def profile():
    """Return a simple HTML page."""
    print("Hit the route!")
    return render_template("profile.html")

@app.route("/survey")
def survey():
    """Return a simple HTML page."""
    print("Hit the route!")
    return render_template("survey.html")

@app.route("/surveyMax")
def surveyMax():
    """Test Survey Page with Popups"""
    print("Im taking a survey")
    return render_template("surveyMax.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True) 
