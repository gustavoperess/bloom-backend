import os
from flask import Flask, jsonify, request
from flask.helpers import get_flashed_messages
from lib.database_connection import get_flask_database_connection
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from dotenv import load_dotenv
from flask_cors import CORS
from lib.repositories.plants_repository import PlantsRepository
from lib.repositories.plants_user_repository import PlantsUserRepository
from lib.models.user import User
from lib.repositories.user_repository import UserRepository
from lib.repositories.help_offer_repository import HelpOfferRepository
from lib.models.help_offer import HelpOffer
from lib.models.help_request import HelpRequest
from lib.repositories.help_request_repository import HelpRequestRepository
from lib.models.received_offer import ReceivedOffer
from lib.repositories.received_offers_repository import ReceivedOffersRepository

# load .env file variables see readme details
load_dotenv()

app = Flask(__name__)
CORS(app)

# Token Setup
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)


# Takes username / email and password from POST request
# Returns authentication token if good match, otherwise 401
@app.route("/token", methods=["POST"])
def create_token():
    # get username or email and password
    username_email = request.json.get("username_email", None)
    password = request.json.get("password", None)

    # query db to ensure user exists:
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)

    # returns user_id if correct, otherwise false
    user_id = user_repository.check_username_or_email_and_password(
        username_email, password
    )

    # catch if username_email / password combination is not in db
    if not user_id:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user_id)
    return jsonify({"token": access_token, "user_id": user_id}), 201


# Takes user details from POST request
# creates user in database
# return 201 if okay, otherwise 401
@app.route("/user/signup", methods=["POST"])
def create_user():
    # NOTE - form validation must be handled on the front end to ensure that
    # appropriate fields are completed. e.g. first_name != "" etc.
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    password_confirm = request.json.get("password_confirm")
    address = request.json.get("address")

    if password == password_confirm:
        try:
            user = User(None, first_name, last_name, username, email, password, address)

            connection = get_flask_database_connection(app)
            user_repository = UserRepository(connection)
            user_repository.add_user_to_db(user)

            return jsonify({"msg": "User created"}), 201
        except:
            return (
                jsonify(
                    {
                        "msg": "Bad request - user not created. This username or email could be taken."
                    }
                ),
                401,
            )

    return (
        jsonify({"msg": "Bad request - user not created. Passwords does not match."}),
        401,
    )


# Takes user_id and returns user_details
@app.route("/user_details/<id>")
def get_user_details(id):
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)
    user = user_repository.get_user_by_id(id)

    print(user)

    if user:
        return (
            jsonify(
                {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "email": user.email,
                    "avatar_url_string": user.avatar_url_string,
                    "address": user.address,
                }
            )
        ), 200
    return jsonify({"msg": "User not found"}), 400


#get all help offers made by a specific user
@app.route("/help_offers/<user_id>", methods=["GET"])
def find_offers_by_user_id(user_id):

    #connect to db and set up offer repository
    connection = get_flask_database_connection(app)
    offer_repository = HelpOfferRepository(connection)

    #returns array of HelpOffer object IDs made by user matching user_id
    offers_by_user = offer_repository.find_by_user(user_id)
    user_offers = []
    for offer in offers_by_user:
        offer_obj = {
            "id": offer.id,
            "user_id": offer.user_id,
            "request_id": offer.request_id,
            "message": offer.message,
            "bid": offer.bid,
            "status": offer.status
        }
        user_offers.append(offer_obj)

    return jsonify(user_offers), 200

#create a new help offer for a help request
@app.route("/help_offers/<help_request_id>", methods=["POST"])
@jwt_required()
def create_help_offer(help_request_id):
    try:
        #connect to db and set up offer repository
        connection = get_flask_database_connection(app)
        offer_repository = HelpOfferRepository(connection)

        #get data from request body and create help_offer in DB
        user_id = request.json.get("user_id")
        request_id = help_request_id
        message = request.json.get("message")
        bid = request.json.get("bid")
        status = request.json.get("status")

        new_offer = HelpOffer(None, user_id, request_id, message, bid, status)

        if None in (user_id, request_id, message, bid, status):
            raise ValueError("All required fields must be filled")    
        offer_repository.create_offer(new_offer)
        return jsonify({"msg": "Help Offer Created"}), 201
    except:
        return jsonify({"msg" : "Help offer creation unsuccessful"}), 400


# return array of offers made to a particular user (user_id)
# UNTESTED
@app.route("/help_offers/help_requests/<user_id>")
# @jwt_required()
def received_help_offers_by_user_id(user_id):
    connection = get_flask_database_connection(app)
    received_offers_repostitory = ReceivedOffersRepository(connection)
    received_offers = received_offers_repostitory.get_all_received_offers_for_user(user_id)
    
    help_offered = []
    for offer in received_offers:
        offer_obj = {
            "help_request_id" : offer.help_request_id,
            "help_request_start_date" : offer.help_request_start_date,
            "help_request_end_date" : offer.help_request_end_date,
            "help_request_name" : offer.help_request_name,
            "help_request_user_id" : offer.help_request_user_id,
            "help_offer_id" : offer.help_offer_id,
            "help_offer_message" : offer.help_offer_message,
            "help_offer_status" : offer.help_offer_status,
            "help_offer_user_id" : offer.help_offer_user_id,
            "help_offer_bid" : offer.help_offer_bid,
            "help_offer_first_name" : offer.help_offer_first_name,
            "help_offer_last_name" : offer.help_offer_last_name,
            "help_offer_avatar_url_string" : offer.help_offer_avatar_url_string,
            "help_offer_username" : offer.help_offer_username,
        }
        help_offered.append(offer_obj)
    return jsonify(help_offered)

# accept help offer
# UNTESTED
@app.route("/help_offers/accept_offer/<help_offer_id>", methods=["PUT"])
# @jwt_required()
def accept_help_offer(help_offer_id):
    connection = get_flask_database_connection(app)
    help_offers_repository = HelpOfferRepository(connection)

    # get list of help_offer_ids associated with request (id to accept excluded) 
    associated_help_offer_ids = help_offers_repository.get_other_help_offer_ids_associated_with_request_id(help_offer_id)
    associated_help_offer_ids.remove(int(help_offer_id))

    # Accept help_offer
    help_offers_repository.accept_help_offer(help_offer_id)

    # Reject other associated help offers
    for help_offer_id in associated_help_offer_ids:
        help_offers_repository.reject_help_offer(help_offer_id)

    return jsonify({"msg" : "Accepted help offer"}), 201

# reject help offer
# UNTESTED
@app.route("/help_offers/reject_offer/<help_offer_id>", methods=["PUT"])
# @jwt_required()
def reject_help_offer(help_offer_id):
    connection = get_flask_database_connection(app)
    help_offers_repository = HelpOfferRepository(connection)
    help_offers_repository.reject_help_offer(help_offer_id)
    return jsonify({"msg" : "Rejected help offer"}), 201
    
# Help Request Routes
@app.route('/help_requests', methods=['GET'])
def get_all_help_requests():
    connection = get_flask_database_connection(app)
    request_repository = HelpRequestRepository(connection)

    all_requests = request_repository.all_requests()
    if all_requests:
        request_data = [
            {
                "id": request.id,
                "date": request.date.strftime("%Y-%m-%d %H:%M:%S"),
                "title": request.title,
                "message": request.message,
                "start_date": request.start_date.strftime("%Y-%m-%d"),
                "end_date": request.end_date.strftime("%Y-%m-%d"),
                "user_id": request.user_id,
                "maxprice": request.maxprice
            }
            for request in all_requests
        ]
        return jsonify(request_data), 200
    return jsonify({"message" : "Unable to find all requests"}), 400

@app.route('/help_requests/<id>', methods=['GET'])
def get_one_help_request_by_id(id):
    connection = get_flask_database_connection(app)
    request_repository = HelpRequestRepository(connection)
    request = request_repository.find_request_by_id(id)
    if request:
        return jsonify({
            "id": request.id,
            "date": request.date.strftime("%Y-%m-%d %H:%M:%S"),
            "title": request.title,
            "message": request.message,
            "start_date": request.start_date.strftime("%Y-%m-%d"),
            "end_date": request.end_date.strftime("%Y-%m-%d"),
            "user_id": request.user_id,
            "maxprice": request.maxprice
        }), 200
    return jsonify({"message" : "Help Request not found"}), 400

@app.route('/help_requests/user/<user_id>', methods=['GET'])
@jwt_required()
def get_all_requests_made_by_one_user(user_id):
    connection = get_flask_database_connection(app)
    request_repository = HelpRequestRepository(connection)
    requests_by_user = request_repository.find_requests_by_user_id(user_id)

    formatted_requests = []
    for request in requests_by_user:
        formatted_request = {
            "id": request.id,
            "date": request.date.strftime("%Y-%m-%d %H:%M:%S"),
            "title": request.title,
            "message": request.message,
            "start_date": request.start_date.strftime("%Y-%m-%d"),
            "end_date": request.end_date.strftime("%Y-%m-%d"),
            "user_id": request.user_id,
            "maxprice": request.maxprice
        }
        formatted_requests.append(formatted_request)
        
    if formatted_requests: 
        return jsonify(formatted_requests), 200
    else:
        return jsonify({"message": "Help requests for current user not found"}), 400


@app.route("/help_requests/create/<user_id>", methods=['POST'])
@jwt_required()
def create_help_request(user_id):
    try:
        connection = get_flask_database_connection(app)
        request_repository = HelpRequestRepository(connection)
        date = request.json.get('date')
        title = request.json.get('title')
        message = request.json.get('message')
        start_date = request.json.get('start_date')
        end_date = request.json.get("end_date")
        maxprice = request.json.get("maxprice")
        if None in (date, title, message, start_date, end_date, maxprice):
            raise ValueError("All required fields must be filled")
        request_repository.create_request(HelpRequest(None, date, title, message, start_date, end_date, user_id, maxprice))
        return jsonify({"message" : "Help request created successfully"}), 200
    except:
        return jsonify({"message" : "Help request creation unsuccessful"}), 400

### PLANTS ROUT ###

# Show all plants in DB
@app.route('/plants', methods=['GET'])
def get_plants():
    connection = get_flask_database_connection(app)
    repository = PlantsRepository(connection)
    plants = repository.all()
    data_json = [{
        "id" : plant.id,
        "common_name" : plant.common_name,
        "latin_name": plant.latin_name,
        "photo": plant.photo,
        "watering_frequency": plant.watering_frequency
        }
    for plant in plants
    ]
    return jsonify(data_json), 200


#Show all plants by user
@app.route('/plants/user/<user_id>', methods=['GET'])
@jwt_required()
def get_plants_by_user(user_id):
    connection = get_flask_database_connection(app)
    repository = PlantsUserRepository(connection)
    plants_with_quantity = repository.find_plants_by_user_id(user_id)
    user_plants = []
    for plant_info in plants_with_quantity:
        plant = plant_info["plant"]
        quantity = plant_info["quantity"]
        plant_obj = {
            "id": plant.id,
            "common_name": plant.common_name,
            "latin_name": plant.latin_name,
            "photo": plant.photo,
            "watering_frequency": plant.watering_frequency,
            "quantity": quantity
        }
        user_plants.append(plant_obj)

    return jsonify(user_plants), 200


@app.route('/plants/user/assign', methods=['POST'])
@jwt_required()
def assign_plant_to_user():
    user_id = request.json.get("user_id")
    plant_id = request.json.get("plant_id")
    quantity = request.json.get("quantity", 1)  # Default quantity to 1 if not specified

    connection = get_flask_database_connection(app)
    repository = PlantsUserRepository(connection)
    repository.assign_plant_to_user(user_id, plant_id, quantity)

    return jsonify({"message": "Plant assigned successfully"}), 200


@app.route('/plants/user/update', methods=['POST'])
@jwt_required()
def update_plants_quantity():
    user_id = request.json.get("user_id")
    plant_id = request.json.get("plant_id")
    new_quantity = request.json.get("new_quantity")

    connection = get_flask_database_connection(app)
    repository = PlantsUserRepository(connection)
    repository.update_plants_quantity(user_id, plant_id, new_quantity)

    return jsonify({"message": "Plant quantity updated successfully"}), 200


@app.route('/plants/user/delete', methods=['DELETE'])
@jwt_required()
def delete_plants_from_user():
    user_id = request.json.get("user_id")
    plant_id = request.json.get("plant_id")

    connection = get_flask_database_connection(app)
    repository = PlantsUserRepository(connection)
    repository.delete_plants_from_user(user_id, plant_id)

    return jsonify({"message": "Plant deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
