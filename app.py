from flask import Flask, render_template, jsonify, request, send_from_directory
import os

app = Flask(__name__)

# Путь к папке с раундами
ROUNDS_PATH = "rounds"
CURRENT_ROUND = 1

# Изначальные очки команд
teams_scores = {
    "Team 1": 0,
    "Team 2": 0,
    "Team 3": 0,
    "Team 4": 0,
}

def get_round_data(round_number):
    round_dir = os.path.join(ROUNDS_PATH, f"round{round_number}")
    if not os.path.exists(round_dir):
        return None

    # Читаем вопрос из текстового файла
    with open(os.path.join(round_dir, "question.txt"), "r", encoding="utf-8") as f:
        question_text = f.read().strip()
        print(question_text)

    # Получаем путь к изображению и аудио
    image_path = os.path.join(round_dir, "image.jpg")
    audio_path = os.path.join(round_dir, "audio.mp3")

    return {
        "question_text": question_text,
        "image_path": f"/round_data/{round_number}/image.jpg",
        "audio_path": f"/round_data/{round_number}/audio.mp3",
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_round_data/<int:round_number>")
def get_round(round_number):
    round_data = get_round_data(round_number)
    if round_data:
        return jsonify(round_data)
    return jsonify({"error": "Round not found"}), 404

@app.route("/update_score", methods=["POST"])
def update_score():
    data = request.json
    team_name = data["team_name"]
    change = data["change"]

    if team_name in teams_scores:
        teams_scores[team_name] += change
        return jsonify({"team_name": team_name, "new_score": teams_scores[team_name]})

    return jsonify({"error": "Team not found"}), 404

@app.route("/scores")
def scores():
    return jsonify(teams_scores)

@app.route("/round_data/<int:round_number>/<filename>")
def serve_round_file(round_number, filename):
    round_dir = os.path.join(ROUNDS_PATH, f"round{round_number}")
    return send_from_directory(round_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)
