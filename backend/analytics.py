'''
This file is where all the data is visualized
'''

#3
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

#3
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

    if not evals:
        return results

    sorted_evals = sorted(evals, key=lambda x: x["score"], reverse=True)
    best_score = sorted_evals[0]["score"] if sorted_evals else 0
    
    for idx, item in enumerate(sorted_evals):
        move = item.get("move")
        score = item.get("score")

        results.append({
            "move": move,
            "score": score,
            "isBest": move == best_move,
            "rank": idx + 1,
            "scoreDiff": best_score - score
        })

    return results


#explanation of the ai's moves
def generate_explanation(score, best_move, evals):

    if score > 0:
        return f"Move {best_move} was chosen because it leads to a favorable position (score: {score})."

    elif score == 0:
        return f"Move {best_move} ensures a draw with optimal play."

    elif score < 0:
        return f"All evaluated moves are unfavorable. Move {best_move} was the least damaging option (score: {score})."

    #fallback: compare moves
    if evals and len(evals) > 1:
        sorted_evals = sorted(evals, key=lambda x: x["score"], reverse=True)
        
        best = sorted_evals[0]
        second = sorted_evals[1]

        diff = best["score"] - second["score"]

        return (
            f"Move {best_move} was selected because it had the highest evaluation score "
            f"({best['score']}). The next best move scored {second['score']}, "
            f"making this move better by {diff}."
        )

    return "The AI chose the move with the best available evaluation."

#replay of the game
def build_replay(move_history):

    replay = []
    #build board as well
    board = [["" for _ in range(3)] for _ in range(3)]

    for i, move in enumerate(move_history):
        row, col = move
        player = "X" if i % 2 == 0 else "O"
        
        board[row][col] = player

        replay.append({
            "moveNumber": i + 1,
            "player": player,
            "position": move,
            #move snapshot
            "board": [r[:] for r in board]
        })

    return replay

#pruning explained
def generate_pruning_insight(metrics, alpha_beta):

    explored = metrics.get("nodesExplored", 0)
    pruned = metrics.get("nodesPruned", 0)

    if not alpha_beta:
        return (
            "Alpha-Beta pruning was disabled. The algorithm explored the full search tree "
            "without eliminating any branches for optimized play."
        )

    if pruned == 0:
        return (
            "Alpha-Beta pruning was enabled, but no branches were pruned. "
            "This can happen when the current game state does not naturally permit early cutoffs."
        )

    total = explored + pruned
    reduction = (pruned / total) * 100 if total > 0 else 0

    return (
        f"Alpha-Beta pruning reduced the search space by approximately {reduction:.1f}%. "
        f"The algorithm explored {explored} nodes and pruned {pruned} nodes that could not affect the final decision."
    )