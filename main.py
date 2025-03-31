from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

flashcards = [
    {
        "id": 1,
        "question": "Who is the most richest person on earth known?",
        "answer": "Elon musk"
    }]


@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/create.html')
def create():
    return render_template('create.html')

@app.route('/edit.html')
def edit():
    return render_template('edit.html')

@app.route('/flashcards', methods=['GET'])
def get_flashcards():
    return jsonify(flashcards)

@app.route('/flashcards', methods=['POST'])
def create_flashcard():
    data = request.json
    new_flashcard = {
        "id": len(flashcards) + 1,
        "question": data["question"],
        "answer": data["answer"]
    }
    flashcards.append(new_flashcard)
    return jsonify(new_flashcard), 201

@app.route('/flashcards/<int:id>', methods=['GET'])
def get_flashcard(id):
    flashcard = next((f for f in flashcards if f["id"] == id), None)
    if flashcard:
        return jsonify(flashcard)
    return jsonify({"error": "Flashcard not found"}), 404

@app.route('/flashcards/<int:id>', methods=['PUT'])
def update_flashcard(id):
    flashcard = next((f for f in flashcards if f["id"] == id), None)
    if not flashcard:
        return jsonify({"error": "Flashcard not found"}), 404

    data = request.json
    flashcard["question"] = data.get("question", flashcard["question"])
    flashcard["answer"] = data.get("answer", flashcard["answer"])
    return jsonify(flashcard)

@app.route('/flashcards/<int:id>', methods=['DELETE'])
def delete_flashcard(id):
    global flashcards
    flashcards = [f for f in flashcards if f["id"] != id]
    return jsonify({"message": "Flashcard deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
