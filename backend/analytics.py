'''
This file is where all the data is visualized
'''

#Main func

def generate_full_analysis(game, board, ai_result, difficulty, alpha_beta, move_history):
#all analytics into one, central aggregator


    summary = generate_summary(game, board, difficulty, alpha_beta, move_history)

    metrics = process_metrics(ai_result.get("metrics", {}))

    move_breakdown = analyze_moves(
        ai_result.get("evals", []),
        ai_result.get("move")
    )

    explanation = generate_explanation(
        ai_result.get("score"),
        ai_result.get("move"),
        ai_result.get("evals", [])
    )

    replay = build_replay(move_history)

    pruning = generate_pruning_insight(metrics, alpha_beta)

    return {
        "summary": summary,
        "metrics": metrics,
        "moveBreakdown": move_breakdown,
        "explanation": explanation,
        "replay": replay,
        "pruningInsight": pruning
    }

#summary of the game, det result+metadata

def generate_summary(game, board, difficulty, alpha_beta, move_history):

    if game.is_winner(board, "O"):
        result = "AI Win"
    elif game.is_winner(board, "X"):
        result = "Human Win"
    elif game.is_draw(board):
        result = "Draw"
    else:
        result = "In Progress"

    return {
        "result": result,
        "difficulty": difficulty,
        "alphaBeta": alpha_beta,
        "totalMoves": len(move_history)
    }


#metrics/normalization

def process_metrics(metrics):

    return {
        "nodesExplored": metrics.get("nodesExplored", 0),
        "nodesPruned": metrics.get("nodesPruned", 0),
        "timeMs": metrics.get("timeMs", 0),
        "depthLimit": metrics.get("depthLimit", 0)
    }


#eval all moves and flags the best

def analyze_moves(evals, best_move):

    results = []

    for item in evals:
        move = item.get("move")
        score = item.get("score")

        results.append({
            "move": move,
            "score": score,
            "isBest": move == best_move
        })

    # sort moves (best first for UI clarity)
    results.sort(key=lambda x: x["score"], reverse=True)

    return results


#explanation of the ai's moves

def generate_explanation(score, best_move, evals):

    if score == 1:
        return f"Move {best_move} was chosen because it guarantees a win."

    elif score == 0:
        return f"Move {best_move} ensures a draw with optimal play."

    elif score == -1:
        return f"All possible moves lead to a loss. Move {best_move} was the least damaging option."

    # fallback: compare scores
    if evals:
        best_score = max(evals, key=lambda x: x["score"])["score"]
        return f"Move {best_move} had the highest evaluation score ({best_score}) among all possible moves."

    return "The AI selected the move with the best available evaluation."

#replay of the game

def build_replay(move_history):

    replay = []

    for i, move in enumerate(move_history):
        player = "X" if i % 2 == 0 else "O"

        replay.append({
            "moveNumber": i + 1,
            "player": player,
            "position": move
        })

    return replay

#pruning explained

def generate_pruning_insight(metrics, alpha_beta):

    explored = metrics.get("nodesExplored", 0)
    pruned = metrics.get("nodesPruned", 0)

    if not alpha_beta:
        return "Alpha-Beta pruning was disabled. All nodes were explored."

    if pruned == 0:
        return "Alpha-Beta pruning was enabled, but no branches were pruned in this move."

    total = explored + pruned
    reduction = (pruned / total) * 100 if total > 0 else 0

    return (
        f"Alpha-Beta pruning explored {explored} nodes and skipped {pruned}, "
        f"reducing the search space by {reduction:.1f}%."
    )