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
        self.nodes_explored += 1
        
        #configuration, using config.json
        ai = config["ai_player"]
        human = config["human_player"]
        depth_limit = config["depth_limit"]
        use_ab = config["use_alpha_beta"]
        
        #evalute terminal state - no moves returned since none left, just score returned
        if self.game.is_terminal(board):
            score = self.game.evaluate_terminal(board, ai, human)
            return score, None, []
        
        #depth-limited heuristic - check if limit reached, use heuristic approx.
        if self.should_use_heuristic(depth, depth_limit):
            score = self.evaluate_board(board, ai, human)
            return score, None, []
        
        moves = self.game.get_available_moves(board)
        best_move = None
        evals = []
        
        #ai's turn (maximizing own score)
        if is_maximizing:
            
            #start with lowest possible score and maximize from there
            best_score = float('-inf')
            
            #loop through moves
            for move in moves:
                #simulate move
                new_board = self.game.apply_move(board, move, ai)
                
                #recursively evaluate opponent response (minimize opponent score)
                score, _, _ = self.minimax(new_board, depth+1, False, alpha, beta, config)
                
                #at root level, store move and its score
                if depth == 0:
                    evals.append({"move": move, "score": score})
                
                #replace best move and associated score if better one found
                if score > best_score:
                    best_score = score
                    best_move = move
                
                #perform a-b pruning
                if use_ab:
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        self.nodes_pruned += 1
                        break
                
                return best_score, best_move, evals
        
        #human's turn (minimizing opponent's score)
        else:
            #start with highest possible score and minimize from there
            best_score = float('inf')
            
            for move in moves:
                #simulate move
                new_board = self.game.apply_move(board, move, human)
                
                #recursively evaluate opponent response (maximize own score)
                score, _, _ = self.minimax(new_board, depth+1, True, alpha, beta, config)
                
                #replace best move and associated score if better one found
                if score < best_score:
                    best_score = score
                    best_move = move
                
                #perform a-b pruning
                if use_ab:
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        self.nodes_pruned += 1
                        break
                
                return best_score, best_move, []
    
    #evaluate heuristics (non-terminal states)
    def evaluate_board(self, board, ai_player, human_player):
        pass
    
    #return depth limit based on chosen difficulty (easy/medium/hard)
    def get_depth_limit(self, difficulty):
        pass
    
    #choose when to stop recursion based on difficulty (depth limit)
    def should_use_heuristic(self, depth, depth_limit):
        pass