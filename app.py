from flask import Flask, request
from flask_cors import CORS
from db_build import DB_init
from queries.races import new_race, get_all_races, one_race, delete_race, update_race
from queries.classes import new_class, get_all_classes, one_class, delete_class, update_class
from queries.proficiencies import new_proficiency


app = Flask(__name__)
CORS(app)


DB_init()


@app.route("/race", methods=['GET', 'POST'])
def race():
    if request.method == "POST":
        try:
            data = request.get_json()
            new_race(data)
            return {"message": "success"}, 200
        except:
            return {"error": "could not create race"}, 400
    else:
        try:
            data = get_all_races()
            return {"data": data}, 200
        except:
            return {"error": "could not retrieve data"}, 400
        
@app.route("/race/<int:i>", methods=['GET', 'PUT', 'DELETE'])
def one_race(i):
    match request.method:
        case "GET":
            data = one_race(i)
            return {"data": data}, 200
        case "DELETE":
            try:
                delete_race(i)
                return {"message": "success"}
            except:
                return {"error": "couldn't delete race"}, 400
        case "PUT":
            try:
                data = request.get_json()
                data["id"] = i
                update_race(data)
                return {"message": "success"}
            except:
                return {"error": "couldn't update race"}, 400
            
@app.route("/class", methods=['GET', 'POST'])
def classes():
    if request.method == "POST":
        try:
            data = request.get_json()
            new_class(data)
            return {"message": "success"}, 200
        except:
            return {"error": "could not create class"}, 400
    else:
        try:
            data = get_all_classes()
            return {"data": data}, 200
        except:
            return {"error": "could not retrieve data"}, 400
        
@app.route("/class/<int:i>", methods=['GET', 'PUT', 'DELETE'])
def one_class(i):
    match request.method:
        case "GET":
            data = one_class(i)
            return {"data": data}, 200
        case "DELETE":
            try:
                delete_class(i)
                return {"message": "success"}
            except:
                return {"error": "couldn't delete class"}, 400
        case "PUT":
            try:
                data = request.get_json()
                data["id"] = i
                update_class(data)
                return {"message": "success"}
            except:
                return {"error": "couldn't update class"}, 400
            
@app.route("/prof", methods=['GET', 'POST'])
def proficiency():
    if request.method == "POST":
        try:
            data = request.get_json()
            #data must include a proficiency field to identify the table being updated
            new_proficiency(data)
            return {"message": "success"}, 200
        except:
            return {"error": "could not create proficiency relationship"}, 400
    else:
        try:
            data = get_all_races()
            return {"data": data}, 200
        except:
            return {"error": "could not retrieve data"}, 400


if __name__ == "__main__":
    # #PROD
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5001)

    #DEV
    app.run(debug=True)