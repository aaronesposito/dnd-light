from flask import Flask, request, jsonify
from flask_cors import CORS
from db_build import DB_init
from queries.races import new_race, get_all_races, get_race, delete_race, update_race
from queries.classes import new_class, get_all_classes, get_class, delete_class, update_class
from queries.proficiencies import new_proficiency, get_all_proficiencies, get_proficiencies_by_type, get_proficiencies_for_class
from queries.characters import create_character, get_all_characters, get_one_character, delete_character, update_character
from queries.accounts import create_user, check_duplicate_username, validate_account
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)


DB_init()






# Standardized response format
def success_response(data=None, message="Success", status_code=200):
    """Create a standardized success response."""
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code


def error_response(message="An error occurred", status_code=400):
    """Create a standardized error response."""
    return jsonify({
        "success": False,
        "error": message
    }), status_code


@app.route("/signup", methods=['POST'])
def register():
    try:
        data = request.get_json()
        user_exists = check_duplicate_username(data["username"])

        if user_exists:
            return error_response(
                message="Account already exists",
            )

        hashed_password = generate_password_hash(data["password"])
        data["password"] = hashed_password
        print(hashed_password)
        user_id = create_user(data)

        return success_response(
            data={"id": user_id},
            message="User created successfully",
            status_code=201
        )
    except Exception as e:
        return error_response(str(e), 400)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    response = validate_account(data["username"])
    if not response["username"] or not check_password_hash(response["password_hash"], data["password"]):
        return {"message": "failed"}
    return {"message": "success"}


# Character endpoints
@app.route("/character", methods=["GET", "POST"])
def character():
    try:
        if request.method == "POST":
            data = request.get_json()
            character_id = create_character(data)
            return success_response(
                data={"id": character_id},
                message="Character created successfully",
                status_code=201
            )
        else:
            characters = get_all_characters()
            return success_response(data=characters)
    except Exception as e:
        return error_response(str(e), 400)


@app.route("/character/<int:i>", methods=["GET", "PUT", "DELETE"])
def one_character(i):
    try:
        match request.method:
            case "GET":
                character = get_one_character(i)
                if character:
                    return success_response(data=character)
                return error_response("Character not found", 404)
            case "PUT":
                data = request.get_json()
                update_character(i, data)
                return success_response(message="Character updated successfully")
            case "DELETE":
                delete_character(i)
                return success_response(message="Character deleted successfully")
    except Exception as e:
        return error_response(str(e), 400)


# Race endpoints
@app.route("/race", methods=['GET', 'POST'])
def race():
    try:
        if request.method == "POST":
            data = request.get_json()
            race_id = new_race(data)
            return success_response(
                data={"id": race_id},
                message="Race created successfully",
                status_code=201
            )
        else:
            races = get_all_races()
            return success_response(data=races)
    except Exception as e:
        return error_response(str(e), 400)


@app.route("/race/<int:i>", methods=['GET', 'PUT', 'DELETE'])
def one_race(i):
    try:
        match request.method:
            case "GET":
                race = get_race(i)
                if race:
                    return success_response(data=race)
                return error_response("Race not found", 404)
            case "PUT":
                data = request.get_json()
                update_race(i, data)
                return success_response(message="Race updated successfully")
            case "DELETE":
                delete_race(i)
                return success_response(message="Race deleted successfully")
    except Exception as e:
        return error_response(str(e), 400)


# Class endpoints
@app.route("/class", methods=['GET', 'POST'])
def classes():
    try:
        if request.method == "POST":
            data = request.get_json()
            class_id = new_class(data)
            return success_response(
                data={"id": class_id},
                message="Class created successfully",
                status_code=201
            )
        else:
            classes = get_all_classes()
            return success_response(data=classes)
    except Exception as e:
        return error_response(str(e), 400)


@app.route("/class/<int:i>", methods=['GET', 'PUT', 'DELETE'])
def one_class(i):
    try:
        match request.method:
            case "GET":
                class_data = get_class(i)
                if class_data:
                    return success_response(data=class_data)
                return error_response("Class not found", 404)
            case "PUT":
                data = request.get_json()
                update_class(i, data)
                return success_response(message="Class updated successfully")
            case "DELETE":
                delete_class(i)
                return success_response(message="Class deleted successfully")
    except Exception as e:
        return error_response(str(e), 400)


# Proficiency endpoints
@app.route("/prof", methods=['GET', 'POST'])
def proficiency():
    try:
        if request.method == "POST":
            data = request.get_json()
            prof_id = new_proficiency(data)
            return success_response(
                data={"id": prof_id},
                message="Proficiency created successfully",
                status_code=201
            )
        else:
            proficiencies = get_all_proficiencies()
            return success_response(data=proficiencies)
    except Exception as e:
        return error_response(str(e), 400)


@app.route("/prof/<prof>/<int:i>", methods=["GET"])
def proficiencies_by_class(prof, i):
    try:
        proficiencies = get_proficiencies_for_class(i, prof)
        return success_response(data=proficiencies)
    except Exception as e:
        return error_response(str(e), 400)


@app.route("/prof/<prof>", methods=["GET"])
def proficiencies_by_type(prof):
    try:
        proficiencies = get_proficiencies_by_type(prof)
        return success_response(data=proficiencies)
    except Exception as e:
        return error_response(str(e), 400)


if __name__ == "__main__":
    # #PROD
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5001)

    #DEV
    app.run(debug=True)
