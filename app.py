from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates")

# Game state
board = [""] * 9
current_player = "X"

# Check winner
def check_winner():
    winning_combinations = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]

    for combo in winning_combinations:
        a, b, c = combo
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    return None

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Handle move
@app.route("/move", methods=["POST"])
def move():
    global current_player

    data = request.json
    idx = data["index"]

    if board[idx] == "":
        board[idx] = current_player

        winner = check_winner()

        # WIN
        if winner:
            return jsonify({
                "status": "win",
                "winner": winner,
                "board": board
            })

        # TIE
        if "" not in board:
            return jsonify({
                "status": "tie",
                "board": board
            })

        # Continue
        current_player = "O" if current_player == "X" else "X"

        return jsonify({
            "status": "continue",
            "board": board,
            "player": current_player
        })

    return jsonify({"status": "invalid"})

# Restart game
@app.route("/restart")
def restart():
    global board, current_player
    board = [""] * 9
    current_player = "X"
    return jsonify({"status": "reset"})

# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
