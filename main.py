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


all_wings = [{"name": "Ain't My Faulks", "description": "Butter, Dry BBQ, Dry Garlic, Dry Ranch"},{"name": "B.A.D.", "description": "Buttered Atomic Dust"}]
@app.route("/search-results/", methods=["POST"])
def search_results():
    """Return a simple HTML page."""
    print("Searching!")
    test_wings = []
    s_term = request.form['searchterm']
    print(s_term)
    #comp_term = "Ain't My Faulks"

    for w in all_wings:
        print("Enter Loop:")
        print(w["name"].lower())        
        name_PR = fuzz.partial_ratio(s_term.lower(),w["name"].lower())
        des_PR = fuzz.partial_ratio(s_term.lower(),w["description"].lower())
        if name_PR > 65 or des_PR >75:
            print("passed!")
            #print(w["name"])
            test_wings.append(w)

    #PR = fuzz.partial_ratio(s_term.lower(),comp_term.lower())
    #print(PR)
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

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True) 
