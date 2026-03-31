from flask import Flask, request, jsonify
from minimax import MinimaxAI
from game import Game
from analytics import generate_full_analysis

#initialize Flask app
app = Flask(__name__)

#create game instance and pass it into AI
game = Game()
ai = MinimaxAI(game)

#POST API endpoint for making move (data sent from frontend)
@app.route("/make-move", methods=["POST"])

#runs when /make-move called
def make_move():
    try:
        #read incoming frontend JSON
        data = request.get_json()
        
        #extract values - board state, difficulty, and if using ab-pruning
        board = data.get("board")
        difficulty = data.get("difficulty", "easy")
        use_alpha_beta = data.get("alphaBeta", True)
        
        move_history = data.get("moveHistory", []) #added for analytics
        #call ai using extracted values from frontend JSON
        result = ai.get_best_move(
            board=board,
            difficulty=difficulty,
            use_alpha_beta=use_alpha_beta
        )
        #more game analysis changes
        analysis = generate_full_analysis(
            game,
            board,
            result,
            difficulty,
            use_alpha_beta,
            move_history
        )
        #Response JSON returned (success)
        return jsonify({
            "success": True,
            "data": result,
            "analysis": analysis

        })
        
    except Exception as e:
        #Response JSON returned (failure)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

#GET endpoint for health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})

#controlled code execution, start Flask server
if __name__ == "__main__":
    app.run(debug=True)