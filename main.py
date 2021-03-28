from flask import Flask, render_template, request, redirect
from fuzzywuzzy import fuzz
from google.cloud import datastore
# FLASK_APP=main.py FLASK_ENV=development flask run

app = Flask(__name__)
datastore_client = datastore.Client("whichwings")

user = "test_user"

dummy = [{"name": "Ace Boogie", "description": "Black Magic, Butter, Dry Ranch"},   
                {"name": "Ain't My Faulks", "description": "Butter, Dry BBQ, Dry Garlic, Dry Ranch"},
                {"name": "B.A.D.", "description": "Buttered Atomic Dust"}]
                
all_wings = [{"name": "Ace Boogie", "description": "Black Magic, Butter, Dry Ranch", "magicNumber": "4194372", "spiceMoistNumber": "10"},   
                {"name": "Ain't My Faulks", "description": "Butter, Dry BBQ, Dry Garlic, Dry Ranch", "magicNumber": "4196418", "spiceMoistNumber": "6"},
                {"name": "B.A.D.", "description": "Butter, Atomic Dust", "magicNumber": "65", "spiceMoistNumber": "10"},
                {"name": "Baby Blues", "description": "Blue Cheese, Frank's Red Hot, Cayenne", "magicNumber": "264", "spiceMoistNumber": "9"},
                {"name": "Big Easy", "description": "Big Shot Bob's Louisiana Licker", "magicNumber": "144", "spiceMoistNumber": "5"},
                {"name": "BigFineWoman2000", "description": "Dark BBQ, Black Magic", "magicNumber": "6", "spiceMoistNumber": "9"},
                {"name": "BigFineWoman3000", "description": "Dark BBQ, Black Magic, Upgraded", "magicNumber": "6", "spiceMoistNumber": "9"},
                {"name": "The Big Picture", "description": "Salt, Butter, Parmesan", "magicNumber": "1048640", "spiceMoistNumber": "6"},
                {"name": "Big Sexy", "description": "Big Shot Bob's Louisiana Licker", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Black and Gold", "description": "Gold BBQ, Black Magic", "magicNumber": "6", "spiceMoistNumber": "9"},
                {"name": "Black and Mild", "description": "Black Magic, Mild Sauce", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Black and Yellow", "description": "Black Magic, Sweet, Honey Mustard", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Black Frank White", "description": "Black Magic, Frank's Red Hot, Ranch", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Black Magic", "description": "Black Magic, Cajun, Butter", "magicNumber": "196", "spiceMoistNumber": "10"},
                {"name": "Black Opts", "description": "The Special Wing Sauce of Cory Freeman", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Cash Club", "description": "Ranch, Garlic, Butter, Parmesan", "magicNumber": "5244992", "spiceMoistNumber": "5"},
                {"name": "The Color Purple", "description": "Raspberry, Garlic", "magicNumber": "8390656", "spiceMoistNumber": "5"},
                {"name": "Cool Runnings", "description": "Jamaican Jerk, Ranch", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Coraopolis Cajun", "description": "Cajun, Mild", "magicNumber": "", "spiceMoistNumber": "10"},
                {"name": "Coraopolis Gunslinger", "description": "Jalapeno, Ranch", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Eye of the Tiger", "description": "Talk of Beaver Falls, Ranch", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Flaming Flamingo", "description": "Garlic, Chili, Ranch, Hot", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Flossin' Season", "description": "Ranch, Lawry's Seasoned Salt", "magicNumber": "4259840", "spiceMoistNumber": "6"},
                {"name": "Frank Sinatra", "description": "Frank's Red Hot, Blue Cheese, Parmesan", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Frank White", "description": "Frank's Red Hot, Ranch", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Frankie Valli", "description": "Frank's Red Hot, Ranch, Parmesan", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Game Changer", "description": "Butter, Parmesan, Ranch", "magicNumber": "", "spiceMoistNumber": "6"},
                {"name": "Gold Fire", "description": "Hot, Gold BBQ", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Honey Bunny", "description": "Sweet, Hot, Chili, Ranch", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Jamaican Frank", "description": "Hot, Jamaican Jerk", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Jamaican Jerk", "description": "Jerk Seasoning, Butter", "magicNumber": "", "spiceMoistNumber": "6"},
                {"name": "Lady Luck", "description": "Hot Sauce, Ranch", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Lake Show", "description": "Raspberry, Honey Mustard", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Lebron to the Lakers", "description": "Black Magic, Raspberry, Honey Mustard", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Magic Man", "description": "Hot Sauce, Black Magic", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Mean Joe Greene", "description": "Black Magic, Gold BBQ, Jalapeno", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Mister C's", "description": "Black Magic, Parmesan", "magicNumber": "", "spiceMoistNumber": "10"},
                {"name": "The Most Interesting Flavor in the World", "description": "Not Hot, Very Interesting", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Mr. Northside", "description": "Honey Mustard, BBQ", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Napoleon", "description": "Sweet, Buffalo", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Napoleon Cajun", "description": "Sweet, Buffalo, Cajun", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Napoleon Complex", "description": "Sweet, Buffalo, Big Shot Bobs Seasoning, ", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Napoleon Dynamite", "description": "Sweet, Buffalo, Cayenne", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Napoleon Garlic", "description": "Sweet, Buffalo, Garlic", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Ole School", "description": "Big Shot Bobs Seasoning, Medium", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Ox's", "description": "BBQ, Jerk Seasoning", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Pigeon Wings", "description": "Sweet, Buffalo, Garlic, Parmesan", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Polish Hill Strangler", "description": "Honey Mustard, Cayenne", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Pookie", "description": "Talk of Beaver Falls, Sweet, Buffalo, Garlic, Parmesan", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Primetime", "description": "Sweet, Hot, Garlic, Golds BBQ", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Showtime", "description": "Salt, Butter", "magicNumber": "", "spiceMoistNumber": "6"},
                {"name": "Steel City", "description": "Mild, Buffalo, Ranch, Parmesan", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Superfly T.N.T.", "description": "Hot, Jamaican Jerk, Ranch", "magicNumber": "", "spiceMoistNumber": "10"},
                {"name": "Talk of Beaver Falls", "description": "Hot, Tangy", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Three Rivers", "description": "Honey Mustard, Ranch, BBQ", "magicNumber": "", "spiceMoistNumber": "5"},
                {"name": "Thunderlips", "description": "Ranch, Atomic Dust", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Too Easy", "description": "Salt, Pepper, Hot Sauce", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Uncle Nick's", "description": "Hot, Spicy, Garlic, Honey, BBQ", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Uncle Rico's", "description": "Sweet, Spicy, Garlic, Honey Mustard", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Walk of Beaver Falls", "description": "Talk of Beaver Falls, Hot", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "Westview Connection", "description": "Big Shot Bobs Seasoning, Cajun, Garlic, Jalapeno", "magicNumber": "", "spiceMoistNumber": "9"},
                {"name": "William Henry Harrison", "description": "Jamaican Jerk, Parmesan", "magicNumber": "", "spiceMoistNumber": "6"},
                {"name": "Wink & Gun", "description": "Hot, Sweet, Ranch", "magicNumber": "", "spiceMoistNumber": "9"}]


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
    do_you_like_these_wings(magic_num, spice_num)
    return redirect("/")

def do_you_like_these_wings(mwn, smp):
    delete_wings()
    #user = session.get("user", None) 
    q = datastore_client.query(kind="Wings")
    all_the_wings = q.fetch()
    #pull list of wings from database
    #for all wings
    print("in do you like, "+mwn+"  "+smp)
    for w in all_the_wings:
    #if smp XXXXX dont add wing
        if (int(w["spiceMoistNumber"]) & int(smp)) == 0:
            if (int(w["magicNumber"]) & int(mwn)) == 0:
                store_wing_pref(user,w["name"],w["description"])
                print(w["name"])

# DELETE: store user's wing preferences
@app.route("/store-wings/", methods=["POST"])
def store_wings():
    # get input wing_preferences
    wing_preferences = all_wings
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
