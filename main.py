from flask import Flask, request, jsonify
import json
import os
import random

app = Flask(__name__)

# Opening a file inside Project folder for pets
def load_pets():
    if os.path.exists("pets.json"):
        with open("pets.json", "r") as file:
            return json.load(file)
    return []

def save_pets():
    if os.path.exists("pets.json"):
        with open("pets.json", "w") as file:
            json.dump(pets_data, file, indent=4)

pets_data = load_pets()

@app.route("/routes", methods=["GET"])
def list_routes():
    routes = []

    for rout in app.url_map.iter_rules():
        routes.append({
            "endpoint": rout.endpoint,
            "methods": list(rout.methods),
            "route": str(rout)
        })
    
    return jsonify(routes)

# Get info about all pets
@app.route("/pets" , methods=["GET"])
def get_pets():
    
    return jsonify(pets_data), 200

# Create a new pet
@app.route("/pets", methods=["POST"])
def create_pet():
    data = request.get_json()

    new_pet = {
        "id": max((pet["id"] for pet in pets_data), default=1) + 1,
        "name": data.get("name"),
        "type": data.get("type"),
        "age": data.get("age", 0),
        "mischief_level": data.get("mischief_level", 5),
        "special_ability": data.get("special_ability", "none"),
        "status": data.get("status", "sleepy")
    }

    pets_data.append(new_pet)
    save_pets()
    return jsonify(new_pet), 201

#Creating more than 1 pet manualy (can be a random or manually created)
@app.route("/pets/bulk_production", methods=["POST"])

def bulk():
    data = request.get_json()

    
    for pet_data in data:
        # If information is not written manualy - random
        new_pets = {
            "id": max((pet["id"] for pet in pets_data), default = 0) + 1,
            "name": pet_data.get("name") or f"Pet{random.randint(1,100)}",
            "type": pet_data.get("type") or random.choice(["cat", "dog"]),
            "age": pet_data.get("age") or random.randint(1,5), 
            "mischief_level": pet_data.get("mischief_level") or random.randint(1, 10),
            "special_ability": pet_data.get("special_ability", "none"),
            "status": pet_data.get("status", "sleepy")
        }
        pets_data.append(new_pets)
    save_pets()
    return jsonify({"message": "Pets created! Welcome your new flyffy (or bald) army"}), 201





@app.route("/pets/<int:pet_id>", methods=["DELETE"])
def delete_pet(pet_id):
    
    pet = next((pet for pet in pets_data if pet["id"] == pet_id), None)
    if pet is None:
        return jsonify({"error": "Pet with this number doesn't exist. Try again!"}), 404
    else:
        pets_data.remove(pet)
        save_pets()
        return jsonify({"message": "It's kinda sad, but... The pet was successfuly removed!"}), 200
    
    
@app.route("/pets/<int:pet_id>", methods=["PUT"])
def update_pet(pet_id):
    data = request.get_json()
    pet = next((p for p in pets_data if p["id"] == pet_id), None)
    if not pet: 
        return jsonify({"error": "Sadly, pet with this id doesn't exist. "})    
    
    pet.update({
        "name": data["name"],
        "type": data["type"],
        "age": data.get("age", 0),
        "mischief_level": data.get("mischiev_level", 5),
        "special_ability": data.get("special_ability", "none"),
        "status": data.get("status", "sleepy")
    })
    save_pets()
    return jsonify({"message": "Information was successfuly updated with PUT!"}), 200

@app.route("/pets/<int:pet_id>", methods=["PATCH"])
def patch_pet(pet_id):
    data = request.get_json()
    pet = next((p for p in pets_data if p["id"] == pet_id), None)
    if not pet: 
        return jsonify({"error": "Sadly, pet with this id doesn't exist. "})
    
    for key in data:
        # Check for a field what the user wrote in the PATCH request. If not - skip
        if key in pet:
            pet[key] = data[key]
    save_pets()
    return jsonify({"message": "You were able to PATCH a pet!"}), 200

@app.route("/pets/<int:pet_id>", methods=["GET"])
def get_pet(pet_id):
    pet = next((pet for pet in pets_data if pet["id"] == pet_id), None)
    # next() is a function that searching for the first element

    if pet is None:
        return jsonify({"error": "Cute pet doesn't exist with this id! Try again!"}), 404
    else:
        return jsonify(pet), 200

# Create a id
@app.route("/pets/<int:pet_id>", methods=["POST"])
def create_id(pet_id):
    data = request.get_json()
    existing_pet = next((pet for pet in pets_data if pet["id"] == pet_id), None)
    if existing_pet:
        return jsonify({"error": "Pet with this id already exist"}), 409
    new_pet = {
        "id": pet_id,
        "name": data.get("name"),
        "type": data.get("type"),
        "age": data.get("age", 0),
        "mischief_level": data.get("mischief_level", 5),
        "special_ability": data.get("special_ability", "none"),
        "status": data.get("status", "sleepy")
    
    }
    pets_data.append(new_pet)
    save_pets()
    return jsonify(new_pet), 201

# Breed a new pet by connecting p1 and p2
@app.route("/pets/breed", methods=["POST"])
def breed_pet():
    data = request.get_json()
    parent1_id = data.get("parent1_id")
    parent2_id = data.get("parent2_id") 

    parent1 = next((pet for pet in pets_data if pet["id"] == parent1_id), None)
    parent2 = next((pet for pet in pets_data if pet["id"] == parent2_id), None)

    
    new_pet = {
        "id": max(pet["id"] for pet in pets_data) + 1, # max id + 1
        "name": parent1["name"][:3] + parent2["name"][:2],
        "type": parent1["type"] if parent1["type"] == parent2["type"] else "hybrid",
        "age": 0,
        "mischief_level": (parent1["mischief_level"] + parent2["mischief_level"]) // 2,
        "special_ability": parent1["special_ability"] if random.choice([True, False]) else parent2["special_ability"],
        "status": "sleepy"
    }

    pets_data.append(new_pet)
    save_pets()
    return jsonify(new_pet), 201

# Filter by type of status of the pet
@app.route("/pets/search", methods=["GET"])
def search_pets():

    type_filter = request.args.get("type")
    status_filter = request.args.get("status")

    results = pets_data

    if type_filter:
        results = [pet for pet in results if pet["type"] == type_filter]
    
    if status_filter:
        results = [pet for pet in results if pet["status"] == status_filter]
    
    return jsonify(results), 200

# create pages
@app.route("/pets/page", methods=["GET"])
def get_pets_page():

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))

    if page < 1:
        page = 1
    if limit < 1:
        limit = 5

    start = (page - 1) * limit
    end = start + limit

    results = pets_data[start:end]
    return jsonify({
        "page": page,
        "limit": limit,
        "total": len(pets_data),
        "results": results,
    }), 200

# Sorting pets and using GET to get information
@app.route("/pets/sort_by", methods=["GET"])
def sort_by():

    sort_by = request.args.get("sort_by")
    order = request.args.get("order", "asc")
    
    results = pets_data

# labda == def get_age(pet): return pet["age"]
    if sort_by:
        reverse = True if order == "desc" else False
        results = sorted(results, key=lambda pet: pet.get(sort_by), reverse=reverse)

    return jsonify(results), 200


@app.route("/pets/random_pet_info", methods=["GET"])
def random_pet_info():
    # just to be sure. If there's no data - error message
    if not pets_data:
        return jsonify({"error": "Well, there's no pets in the list, I assume? Or something went wrong... Try to check the list of all pets, maybe?"})
    
    pet = random.choice(pets_data)

    return jsonify(pet), 200

@app.route("/pets/fight", methods=["POST"])
def fight():
    data = request.get_json()
    pet1_id = data.get("pet1_id")
    pet2_id = data.get("pet2_id")

    pet1 = next((pet for pet in pets_data if pet["id"] == pet1_id), None)
    pet2 = next((pet for pet in pets_data if pet["id"] == pet2_id), None)

    pet1_str = pet1["age"] + pet1["mischief_level"]
    pet2_str = pet2["age"] + pet2["mischief_level"]
    results = pet1_str - pet2_str
    if pet1_str > pet2_str:
        return jsonify({"winner": pet1_id})
    
    else:
        return jsonify({"winner": pet2_id})
    


if __name__ == "__main__":
    app.run(debug=True)