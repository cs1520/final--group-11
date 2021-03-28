from flask import Flask, render_template, request, redirect
from fuzzywuzzy import fuzz
from google.cloud import datastore
# FLASK_APP=main.py FLASK_ENV=development flask run

app = Flask(__name__)
datastore_client = datastore.Client("whichwings")

dummy = [{"name": "Ace Boogie", "description": "Black Magic, Butter, Dry Ranch"},   
                {"name": "Ain't My Faulks", "description": "Butter, Dry BBQ, Dry Garlic, Dry Ranch"},
                {"name": "B.A.D.", "description": "Buttered Atomic Dust"}]
                
all_wings = [{"name": "Ace Boogie", "description": "Black Magic, Butter, Dry Ranch", "magicNumber": "4194372", "spiceMoistNumber": "9"},   
                {"name": "Ain't My Faulks", "description": "Butter, Dry BBQ, Dry Garlic, Dry Ranch", "magicNumber": "4196418", "spiceMoistNumber": "5"},
                {"name": "B.A.D.", "description": "Butter, Atomic Dust", "magicNumber": "65", "spiceMoistNumber": "9"},
                {"name": "Black Magic", "description": "Black Magic, Cajun, Butter", "magicNumber": "196", "spiceMoistNumber": "9"},
                {"name": "The Big Picture", "description": "Salt, Butter, Parmesan", "magicNumber": "1048640", "spiceMoistNumber": "5"},
                {"name": "Flossin' Season", "description": "Ranch, Lawry's Seasoned Salt", "magicNumber": "4259840", "spiceMoistNumber": "5"},
                {"name": "Baby Blues", "description": "Blue Cheese, Frank's Red Hot, Cayenne", "magicNumber": "264", "spiceMoistNumber": "10"},
                {"name": "Big Easy", "description": "Big Shot Bob's Louisiana Licker", "magicNumber": "144", "spiceMoistNumber": "6"},
                {"name": "BigFineWoman2000", "description": "Dark BBQ, Black Magic", "magicNumber": "6", "spiceMoistNumber": "10"},
                {"name": "The Color Purple", "description": "Raspberry, Garlic", "magicNumber": "8390656", "spiceMoistNumber": "6"},
                {"name": "Black and Gold", "description": "Gold BBQ, Black Magic", "magicNumber": "6", "spiceMoistNumber": "10"},
                {"name": "Cash Club", "description": "Ranch, Garlic, Butter, Parmesan", "magicNumber": "5244992", "spiceMoistNumber": "6"}]


@app.route("/")
def home():
    """Return a simple HTML page."""
    print("Hit the route!")
    users_wings = get_wings()
    return render_template("index.html", picks=users_wings)

@app.route("/search")
def search():
    """Return a simple HTML page."""
    print("Search route!")
    return render_template("search.html", wings=[])

@app.route("/search-results/", methods=["POST"])
def search_results():
    """Return a simple HTML page."""
    print("Searching!")
    test_wings = []
    s_term = request.form['searchterm']
    s_term = s_term.split(',')
    #print(s_term)

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
        #print(tot_des_PR)
        if name_PR > 75 or tot_des_PR > 75:
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

@app.route("/profile-results", methods=["POST"])
def profile_results():
    magic_num = request.args.get('mwn')
    spice_num = request.args.get('smp')
    print(magic_num)
    print(spice_num)
    do_you_like_these_wings(magic_num, spice_num)
    return redirect("/")

def do_you_like_these_wings(mwn, smp):
    #user = session.get("user", None) 
    user = "test_user"
    q = datastore_client.query(kind="Wings")
    all_the_wings = q.fetch()
    #pull list of wings from database
    #for all wings
    for w in all_the_wings:
        w["smp"]
    #if smp XXXXX dont add wing
    #else
        if (w["mwn"] & mwn) == 0:
            store_wing_pref(user,w["name"],w["description"])
# DELETE: store user's wing preferences
@app.route("/store-wings/", methods=["POST"])
def store_wings():
    # get input wing_preferences
    wing_preferences = all_wings
    user = "test_user2"
    #user = session.get("user", None)    
    for w in wing_preferences:
        store_wing_pref(user, w["name"], w["description"])
    return redirect("/")

# store a single wing preference        
def store_wing_pref(user, name, description):
    wing_pref_key = datastore_client.key("Wing Pref")
    wing_pref = datastore.Entity(key=wing_pref_key)
    wing_pref["user"] = user
    wing_pref["wing_name"] = name
    wing_pref["wing_description"] = description
    datastore_client.put(wing_pref)

# get user's preferences
def get_wings():
    #user = session.get("user", None) 
    user = "test_user"
    q = datastore_client.query(kind="Wing Pref")
    q.add_filter("user", "=", user)
    wings = q.fetch()
    users_wings = []
    for w in wings:
        wing_entry = {"name":w["wing_name"], "description":w["wing_description"]}        
        users_wings.append(wing_entry)
    #print(users_wings)
    return users_wings

# delete user's wing preferences        
def delete_wings():
    #user = session.get("user", None) 
    user = "test_user2"
    q = datastore_client.query(kind="Wing Pref")
    q.add_filter("user", "=", user)
    q.keys_only()
    wings = q.fetch()
    for w in wings:
        datastore_client.delete(w)

# store all the wings       
def store_allwings():
    for w in all_wings:
        wing_key = datastore_client.key("Wings")
        wing = datastore.Entity(key=wing_key)
        wing["name"] = w["name"]
        wing["description"] = w["description"]
        wing["magicNumber"] = w["magicNumber"]
        wing["spiceMoistNumber"] = w["spiceMoistNumber"] 
        datastore_client.put(wing)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True) 
