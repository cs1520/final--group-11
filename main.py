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
                
all_wings = [{"name": "Ace Boogie", "description": "Black Magic, Butter, Dry Ranch", "magicNumber": "4194372", "spiceMoistNumber": "10", "type": "Signature"},   
                {"name": "Ain't My Faulks", "description": "Butter, Dry BBQ, Dry Garlic, Dry Ranch", "magicNumber": "4196418", "spiceMoistNumber": "6", "type": "Signature"},
                {"name": "B.A.D.", "description": "Butter, Atomic Dust", "magicNumber": "65", "spiceMoistNumber": "10", "type": "Signature"},
                {"name": "Baby Blues", "description": "Blue Cheese, Frank's Red Hot, Cayenne", "magicNumber": "264", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Big Easy", "description": "Big Shot Bob's Louisiana Licker", "magicNumber": "268435456", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "BigFineWoman2000", "description": "Dark BBQ, Black Magic", "magicNumber": "6", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "BigFineWoman3000", "description": "Dark BBQ, Black Magic, Upgraded", "magicNumber": "6", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "The Big Picture", "description": "Salt, Butter, Parmesan", "magicNumber": "1048640", "spiceMoistNumber": "6", "type": "Signature"},
                {"name": "Big Sexy", "description": "Mark's Signature Flavor", "magicNumber": "268435456", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Black and Gold", "description": "Gold BBQ, Black Magic", "magicNumber": "6", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Black and Mild", "description": "Black Magic, Mild Sauce", "magicNumber": "4", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Black and Yellow", "description": "Black Magic, Sweet, Honey Mustard", "magicNumber": "33562628", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Black Frank White", "description": "Black Magic, Frank's Red Hot, Ranch", "magicNumber": "4194308", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Black Magic", "description": "Black Magic, Cajun, Butter", "magicNumber": "196", "spiceMoistNumber": "10", "type": "Signature"},
                {"name": "Black Opts", "description": "The Special Wing Sauce of Cory Freeman", "magicNumber": "268435456", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Cash Club", "description": "Ranch, Garlic, Butter, Parmesan", "magicNumber": "5244992", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "The Color Purple", "description": "Raspberry, Garlic", "magicNumber": "8390656", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Cool Runnings", "description": "Jamaican Jerk, Ranch", "magicNumber": "4227136", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Coraopolis Cajun", "description": "Cajun, Mild", "magicNumber": "128", "spiceMoistNumber": "10", "type": "Signature"},
                {"name": "Coraopolis Gunslinger", "description": "Jalapeno, Ranch", "magicNumber": "4210688", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Eye of the Tiger", "description": "Talk of Beaver Falls, Ranch", "magicNumber": "272629760", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Flaming Flamingo", "description": "Garlic, Chili, Ranch, Hot", "magicNumber": "4196864", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Flossin' Season", "description": "Ranch, Lawry's Seasoned Salt", "magicNumber": "4259840", "spiceMoistNumber": "6", "type": "Signature"},
                {"name": "Frank Sinatra", "description": "Frank's Red Hot, Blue Cheese, Parmesan", "magicNumber": "1048584", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Frank White", "description": "Frank's Red Hot, Ranch", "magicNumber": "4194304", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Frankie Valli", "description": "Frank's Red Hot, Ranch, Parmesan", "magicNumber": "5242880", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Game Changer", "description": "Butter, Parmesan, Ranch", "magicNumber": "5242944", "spiceMoistNumber": "6", "type": "Signature"},
                {"name": "Gold Fire", "description": "Hot, Gold BBQ", "magicNumber": "2", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Honey Bunny", "description": "Sweet, Hot, Chili, Ranch", "magicNumber": "37749248", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Jamaican Frank", "description": "Hot, Jamaican Jerk", "magicNumber": "32832", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Jamaican Jerk", "description": "Jerk Seasoning, Butter", "magicNumber": "32832", "spiceMoistNumber": "6", "type": "Signature"},
                {"name": "Lady Luck", "description": "Hot Sauce, Ranch", "magicNumber": "4194304", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Lake Show", "description": "Raspberry, Honey Mustard", "magicNumber": "8396800", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Lebron to the Lakers", "description": "Black Magic, Raspberry, Honey Mustard", "magicNumber": "8396804", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Magic Man", "description": "Hot Sauce, Black Magic", "magicNumber": "4", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Mean Joe Greene", "description": "Black Magic, Gold BBQ, Jalapeno", "magicNumber": "16390", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Mister C's", "description": "Black Magic, Parmesan", "magicNumber": "1048580", "spiceMoistNumber": "10", "type": "Signature"},
                {"name": "The Most Interesting Flavor in the World", "description": "Not Hot, Very Interesting", "magicNumber": "268435456", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Mr. Northside", "description": "Honey Mustard, BBQ", "magicNumber": "8194", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Napoleon", "description": "Sweet, Buffalo", "magicNumber": "33554464", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Napoleon Cajun", "description": "Sweet, Buffalo, Cajun", "magicNumber": "33554592", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Napoleon Complex", "description": "Sweet, Buffalo, Big Shot Bobs Seasoning", "magicNumber": "33554480", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Napoleon Dynamite", "description": "Sweet, Buffalo, Cayenne", "magicNumber": "33554720", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Napoleon Garlic", "description": "Sweet, Buffalo, Garlic", "magicNumber": "33556512", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Ole School", "description": "Big Shot Bobs Seasoning, Medium", "magicNumber": "16", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Ox's", "description": "BBQ, Jerk Seasoning", "magicNumber": "32770", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Pigeon Wings", "description": "Sweet, Buffalo, Garlic, Parmesan", "magicNumber": "34605088", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Polish Hill Strangler", "description": "Honey Mustard, Cayenne", "magicNumber": "8448", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Pookie", "description": "Talk of Beaver Falls, Sweet, Buffalo, Garlic, Parmesan", "magicNumber": "303040544", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Primetime", "description": "Sweet, Hot, Garlic, Golds BBQ", "magicNumber": "33556482", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Showtime", "description": "Salt, Butter", "magicNumber": "64", "spiceMoistNumber": "6", "type": "Signature"},
                {"name": "Steel City", "description": "Mild, Buffalo, Ranch, Parmesan", "magicNumber": "5242912", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Superfly T.N.T.", "description": "Hot, Jamaican Jerk, Ranch", "magicNumber": "4227072", "spiceMoistNumber": "10", "type": "Signature"},
                {"name": "Talk of Beaver Falls", "description": "Hot, Tangy", "magicNumber": "268435456", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Three Rivers", "description": "Honey Mustard, Ranch, BBQ", "magicNumber": "4202498", "spiceMoistNumber": "5", "type": "Signature"},
                {"name": "Thunderlips", "description": "Ranch, Atomic Dust", "magicNumber": "4194305", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Too Easy", "description": "Salt, Pepper, Hot Sauce", "magicNumber": "2097152", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Uncle Nick's", "description": "Hot, Spicy, Garlic, Honey, BBQ", "magicNumber": "6146", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Uncle Rico's", "description": "Sweet, Spicy, Garlic, Honey Mustard", "magicNumber": "33564672", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Walk of Beaver Falls", "description": "Talk of Beaver Falls, Hot", "magicNumber": "268435456", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "Westview Connection", "description": "Big Shot Bobs Seasoning, Cajun, Garlic, Jalapeno", "magicNumber": "18576", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "William Henry Harrison", "description": "Jamaican Jerk, Parmesan", "magicNumber": "1081408", "spiceMoistNumber": "6", "type": "Signature"},
                {"name": "Wink & Gun", "description": "Hot, Sweet, Ranch", "magicNumber": "37748736", "spiceMoistNumber": "9", "type": "Signature"},
                {"name": "BBQ", "description": "", "magicNumber": "2", "spiceMoistNumber": "8", "type": "Classic"},
                {"name": "BBQ Ranch", "description": "", "magicNumber": "4194306", "spiceMoistNumber": "8", "type": "Classic"},
                {"name": "Bob's Honey Mustard", "description": "", "magicNumber": "8192", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Bob's Signature Hot", "description": "", "magicNumber": "768", "spiceMoistNumber": "6", "type": "Classic"},
                {"name": "Cajun", "description": "", "magicNumber": "128", "spiceMoistNumber": "4", "type": "Classic"},
                {"name": "Cajun Garlic", "description": "", "magicNumber": "2176", "spiceMoistNumber": "4", "type": "Classic"},
                {"name": "Cajun Ranch", "description": "", "magicNumber": "4194432", "spiceMoistNumber": "4", "type": "Classic"},
                {"name": "Dark BBQ", "description": "", "magicNumber": "2", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Frank's Red Hot", "description": "", "magicNumber": "768", "spiceMoistNumber": "6", "type": "Classic"},
                {"name": "Garlic Butter", "description": "", "magicNumber": "2112", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Garlic Butter Parm", "description": "", "magicNumber": "1050688", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Garlic Parm", "description": "", "magicNumber": "1050624", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Garlic Ranch", "description": "", "magicNumber": "4196352", "spiceMoistNumber": "8", "type": "Classic"},
                {"name": "Gold BBQ", "description": "", "magicNumber": "2", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Honey BBQ", "description": "", "magicNumber": "4098", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Honey Cajun", "description": "", "magicNumber": "4224", "spiceMoistNumber": "6", "type": "Classic"},
                {"name": "Honey Dijon", "description": "", "magicNumber": "5120", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Honey Garlic", "description": "", "magicNumber": "6144", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Honey Old Bay", "description": "", "magicNumber": "528384", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Honey Ranch", "description": "", "magicNumber": "4198400", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Hot Cajun", "description": "", "magicNumber": "128", "spiceMoistNumber": "6", "type": "Classic"},
                {"name": "Hot Garlic", "description": "", "magicNumber": "2048", "spiceMoistNumber": "6", "type": "Classic"},
                {"name": "Hot Garlic Parm", "description": "", "magicNumber": "1050624", "spiceMoistNumber": "6", "type": "Classic"},
                {"name": "Hot Honey", "description": "", "magicNumber": "4096", "spiceMoistNumber": "6", "type": "Classic"},
                {"name": "Hot Honey Garlic", "description": "", "magicNumber": "6144", "spiceMoistNumber": "6", "type": "Classic"},
                {"name": "Hot Old Bay", "description": "", "magicNumber": "524288", "spiceMoistNumber": "6", "type": "Classic"},
                {"name": "Hot Ranch", "description": "", "magicNumber": "4194304", "spiceMoistNumber": "6", "type": "Classic"},
                {"name": "Hottest of the Hot", "description": "", "magicNumber": "384", "spiceMoistNumber": "6", "type": "Classic"},
                {"name": "Lemon Pepper", "description": "", "magicNumber": "2228224", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Lemon Pepper Parm", "description": "", "magicNumber": "3276800", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Lemon Pepper Ranch", "description": "", "magicNumber": "6422528", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Medium Garlic Parm", "description": "", "magicNumber": "1050624", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Mild Garlic Parm", "description": "", "magicNumber": "1050624", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Mild Old Bay", "description": "", "magicNumber": "524288", "spiceMoistNumber": "9", "type": "Classic"},
                {"name": "Mild Ranch", "description": "", "magicNumber": "4194304", "spiceMoistNumber": "9", "type": "Classic"},
                {"name": "Montreal", "description": "", "magicNumber": "262144", "spiceMoistNumber": "8", "type": "Classic"},
                {"name": "Old Bay", "description": "", "magicNumber": "524288", "spiceMoistNumber": "8", "type": "Classic"},
                {"name": "Old Bay Ranch", "description": "", "magicNumber": "4718592", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Peppercorn Ranch", "description": "", "magicNumber": "6291456", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Peppercorn Ranch Parm", "description": "", "magicNumber": "7340032", "spiceMoistNumber": "10", "type": "Classic"},
                {"name": "Ranch", "description": "", "magicNumber": "4194304", "spiceMoistNumber": "8", "type": "Classic"},
                {"name": "Salt and Pepper", "description": "", "magicNumber": "2097152", "spiceMoistNumber": "9", "type": "Classic"},
                {"name": "Salt and Vinegar", "description": "", "magicNumber": "134217728", "spiceMoistNumber": "9", "type": "Classic"},
                {"name": "Seasoned", "description": "", "magicNumber": "16777216", "spiceMoistNumber": "9", "type": "Classic"},
                {"name": "Teriyaki", "description": "", "magicNumber": "67108864", "spiceMoistNumber": "10", "type": "Classic"}]

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
    print("in do you like, "+mwn+"  "+smp)
    for w in all_the_wings:
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
