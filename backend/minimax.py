'''
This file handles minimax algorithm logic, AB-pruning, difficulty,
heuristics, and metrics tracking.
'''

import time

class MinimaxAI:
    
    def __init__(self, game):
        self.game = game
        self.nodes_explored = 0
        self.nodes_pruned = 0
        self.start_time = 0
        self.end_time = 0
    
    #returns best move and analysis data
    def get_best_move(self, board, difficulty, use_alpha_beta):
        
        #reset metrics
        self.nodes_explored = 0
        self.nodes_pruned = 0
        self.start_time = time.time()
        
        ai_player = "O"
        human_player = "X"
        
        #determine depth limit using difficulty
        depth_limit = self.get_depth_limit(difficulty)
        
        #build config.json file
        config = {
            "ai_player": ai_player,
            "human_player": human_player,
            "depth_limit": depth_limit,
            "use_alpha_beta": use_alpha_beta,
        }
        
        #call minimax algorithm and return info
        best_score, best_move, evals = self.minimax(
            board, 0, True, float('-inf'), float('inf'), config
        )
        
        #end timer after calculations done
        self.end_time = time.time()
        
        #returns JSON of structured result (evals stores best moves)
        return {
            "move": best_move,
            "score": best_score,
            "metrics": {
                "nodesExplore": self.nodes_explored,
                "nodesPruned": self.nodes_pruned,
                "timeMs": int((self.end_time - self.start_time) * 1000),
                "depthLimit": depth_limit
            },
            "evals": evals
        }
        
    #main minimax function (recursive)
    def minimax(self, board, depth, is_maximizing, alpha, beta, config):
        pass
    
    #evaluate heuristics (non-terminal states)
    def evaluate_board(self, board, ai_player, human_player):
        pass
    
    #return depth limit based on chosen difficulty (easy/medium/hard)
    def get_depth_limit(self, difficulty):
        pass
    
    #choose when to stop recursion based on difficulty (depth limit)
    def should_use_heuristic(self, depth, depth_limit):
        pass