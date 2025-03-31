from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample flashcards stored in-memory (Temporary database)
flashcards = [
    {"id": 1, "question": "What is Flask?", "answer": "A micro web framework for Python"},
    {"id": 2, "question": "What is an API?", "answer": "Application Programming Interface"}
]

# 🔹 1. GET /flashcards - Retrieve all flashcards
@app.route('/flashcards', methods=['GET'])
def get_flashcards():
    return jsonify(flashcards)

# 🔹 2. POST /flashcards - Create a new flashcard
@app.route('/flashcards', methods=['POST'])
def create_flashcard():
    data = request.json
    new_flashcard = {
        "id": len(flashcards) + 1,  # Auto-increment ID
        "question": data["question"],
        "answer": data["answer"]
    }
    flashcards.append(new_flashcard)
    return jsonify(new_flashcard), 201

# 🔹 3. GET /flashcards/<id> - Get a single flashcard by ID
@app.route('/flashcards/<int:id>', methods=['GET'])
def get_flashcard(id):
    flashcard = next((f for f in flashcards if f["id"] == id), None)
    if flashcard:
        return jsonify(flashcard)
    return jsonify({"error": "Flashcard not found"}), 404

# 🔹 4. PUT /flashcards/<id> - Update a flashcard
@app.route('/flashcards/<int:id>', methods=['PUT'])
def update_flashcard(id):
    flashcard = next((f for f in flashcards if f["id"] == id), None)
    if not flashcard:
        return jsonify({"error": "Flashcard not found"}), 404

    data = request.json
    flashcard["question"] = data.get("question", flashcard["question"])
    flashcard["answer"] = data.get("answer", flashcard["answer"])
    return jsonify(flashcard)

# 🔹 5. DELETE /flashcards/<id> - Delete a flashcard
@app.route('/flashcards/<int:id>', methods=['DELETE'])
def delete_flashcard(id):
    global flashcards
    flashcards = [f for f in flashcards if f["id"] != id]
    return jsonify({"message": "Flashcard deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)  # Runs on localhost
