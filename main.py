from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
uri = os.getenv("mongo_uri")
client = MongoClient(uri)

db = client["flashcards_db"]
collection = db["flashcards"]
groups = db["groups"]

@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/index_editor.html')
def editor():
    return render_template('index_editor.html')

@app.route('/create.html')
def create():
    groups_list = list(groups.find({}, {"name": 1}))
    return render_template('create.html', groups=groups_list)

@app.route('/edit.html')
def edit():
    return render_template('edit.html')

@app.route('/flashcards', methods=['GET'])
def get_flashcards():
    flashcards = list(collection.find({}, {"_id": 0}))
    return jsonify(flashcards)

@app.route('/groups.html')
def groups_page():
    return render_template('groups.html')

@app.route('/flashcards', methods=['POST'])
def create_flashcard():
    data = request.json
    new_flashcard = {
        "question": data["question"],
        "answer": data["answer"],
        "group_id": data["group_id"]
    }
    result = collection.insert_one(new_flashcard)
    new_flashcard["_id"] = str(result.inserted_id) 

    return jsonify(new_flashcard), 201

@app.route('/create_group', methods=['POST'])
def create_group():
    data = request.json
    new_group = {
        "name": data["name"]
    }
    result = groups.insert_one(new_group)
    new_group["_id"] = str(result.inserted_id)

    return jsonify(new_group), 201
    

@app.route('/flashcards/<int:id>', methods=['GET'])
def get_flashcard(id):
    flashcard = collection.find_one({"id": id}, {"_id": 0})
    if flashcard:
        return jsonify(flashcard)
    return jsonify({"error": "Flashcard not found"}), 404

@app.route('/flashcards/<int:id>', methods=['PUT'])
def update_flashcard(id):
    data = request.json
    updated_data = {"$set": {}}

    if "question" in data:
        updated_data["$set"]["question"] = data["question"]
    if "answer" in data:
        updated_data["$set"]["answer"] = data["answer"]

    result = collection.update_one({"id": id}, updated_data)

    if result.modified_count == 0:
        return jsonify({"error": "Flashcard not found"}), 404

    updated_flashcard = collection.find_one({"id": id}, {"_id": 0})
    return jsonify(updated_flashcard)

@app.route('/flashcards/<int:id>', methods=['DELETE'])
def delete_flashcard(id):
    result = collection.delete_one({"id": id})

    if result.deleted_count == 0:
        return jsonify({"error": "Flashcard not found"}), 404

    return jsonify({"message": "Flashcard deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
