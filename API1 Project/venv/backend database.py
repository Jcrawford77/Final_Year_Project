from flask import Flask, json,jsonify, make_response, request
from pymongo import MongoClient
from bson import ObjectId, objectid
import jwt
import datetime
from functools import wraps
import bcrypt
from flask_cors import CORS

#This is for my Token Generation and user access.
#This will be utilized further into development once the frontend of my system
#has been further developed

def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token= request.headers['x-access-token']

        if not token:
            return jsonify({'message' :'Token missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid'}), 401
        return func(*args, **kwargs)
    return jwt_required_wrapper



app = Flask(__name__)
CORS(app)


app.config['SECRET_KEY'] = 'mysecret'


#This is the connection needed for my backend to connect to my databases
#'premier_league' refers to my database inc. 20 teams.
#'chelsea' referes to the databse containing the Chelsea squad
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.premier_league
teams = db.league
db = client.chelsea
players= db.players


#Below is the CRUD functionality for my system.
#First is to read all the teams from my database

@app.route("/api/v1.0/league", methods = ["GET"])
def show_all_teams():
    page_num, page_size = 1, 25
    if request.args.get("pn"):
        page_num = int(request.args.get('pn'))
    if request.args.get("ps"):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))

    data_to_return = []
    for team in teams.find().skip(page_start).limit(page_size):
        team['_id'] = str(team['_id'])
        data_to_return.append(team)
        
    return make_response( jsonify( data_to_return ), 200)




#This is to read one team from the database using a unique term
@app.route("/api/v1.0/league/<string:Team>", methods = ["GET"])
def show_one_team(Team):
    team = teams.find_one( { "_id" : ObjectId(Team)})
    if team is not None:
        team["_id"] = str(team["_id"])
    
        return make_response( jsonify(team), 200)
    else:
        return make_response(jsonify({"error" : "Invalid Team"}), 404)



#This is to create a new team to go into the database
@app.route("/api/v1.0/league", methods = ["POST"])
def add_new_team():
    if "Team" in request.form and "Games Played" in request.form and "Goal Difference" in request.form and "xG" in request.form and "xGA" in request.form and "Net xG" in request.form and "xG Points" in request.form and "Points" in request.form: 
        new_team = {
            "Team" : request.form["Team"],
            "Games Played": request.form["Games Played"],
            "Goal Difference": request.form["Goal Difference"],
            "xG": request.form["xG"],
            "xGA": request.form["xGA"],
            "Net xG": request.form["Net xG"],
            "xG Points": request.form["xG Points"],
            "Points": request.form["Points"]
        }
        new_team_id=teams.insert_one(new_team)
        new_team_link= "http://127.0.0.1:5000/api/v1.0/league/" + \
            str(new_team_id.inserted_id)
        return make_response(jsonify( { "url" : new_team_link }), 201)
    else:
        return make_response(jsonify ({ "error" : "Missing Form Data"}), 404)



#This is to delete a stored team from the database
@app.route("/api/v1.0/league/<string:Team>", methods = ["DELETE"])
def delete_team(Team):
    result = teams.delete_one({ "_id" : ObjectId(Team)})
    if result.deleted_count == 1:
        return make_response( jsonify({}), 204 )
    else:
        return make_response( jsonify( {"error" : "Invalid Team"}), 404 )













# This is to introduce the same functionality again but for my second database


#This reads the database for all players within the Chelsea squad
@app.route("/api/v1.0/players", methods = ["GET"])
def show_all_players():
    page_num, page_size = 1, 25
    if request.args.get("pn"):
        page_num = int(request.args.get('pn'))
    if request.args.get("ps"):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))

    data_to_return = []
    for player in players.find().skip(page_start).limit(page_size):
        player['_id'] = str(player['_id'])
        data_to_return.append(player)
        
    return make_response( jsonify( data_to_return ), 200)




#This reads one individual Chelsea player from the database
@app.route("/api/v1.0/players/<string:Players>", methods = ["GET"])
def show_one_player(Players):
    player = players.find_one( { "_id" : ObjectId(Players)})
    if player is not None:
        player["_id"] = str(player["_id"])
    
        return make_response( jsonify( [player] ), 200)
    else:
        return make_response(jsonify({"error" : "Invalid Player"}), 404)




#This creates a new player to be stored inside the database
@app.route("/api/v1.0/players", methods = ["POST"])
def add_new_player():
    if "Player" in request.form and "Apps" in request.form and "Goals" in request.form and "Min" in request.form and "Position" in request.form and "sh90" in request.form and "xA90" in request.form and "xG" in request.form and "xG90" in request.form: 
        new_player = {
            "Player" : request.form["Player"],
            "Apps": request.form["Apps"],
            "Goals": request.form["Goals"],
            "Min": request.form["Min"],
            "Position": request.form["Position"],
            "sh90": request.form["sh90"],
            "xA90": request.form["xA90"],
            "xG": request.form["xG"],
            "xG90": request.form["xG90"]

        }
        new_player_id=players.insert_one(new_player)
        new_player_link= "http://127.0.0.1:5000/api/v1.0/players/" + \
            str(new_player_id.inserted_id)
        return make_response(jsonify( { "url" : new_player_link }), 201)
    else:
        return make_response(jsonify ({ "error" : "Missing Form Data"}), 404)




#This deletes a stored player from the database
@app.route("/api/v1.0/players/<string:Players>", methods = ["DELETE"])
def delete_player(Players):
    result = teams.delete_one({ "_id" : ObjectId(Players)})
    if result.deleted_count == 1:
        return make_response( jsonify({}), 204 )
    else:
        return make_response( jsonify( {"error" : "Invalid Player"}), 404 )














#This allows for user logins, which will be demonstrated more clearly
#Once the Frontend has been futher developed
@app.route("/api/v1.0/login", methods=["GET"])
def login():
    auth = request.authorization
    if auth and auth.password =='password':
        token = jwt.encode( {'user' :auth.username,'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify( { 'token' : token.decode('UTF-8')})
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm ="Login Required"'})


if __name__ == "__main__":
    app.run(debug=True)