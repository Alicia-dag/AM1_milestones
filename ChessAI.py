"""
Handling the AI moves.
"""
import random

import tkinter as tk    # Imports the tkinter module
from tkinter import ttk # Imports the ttk module


piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}   # The value of each piece


#######################################################################################################
##                                      PIECE SQUARE TABLES                                         ##
#######################################################################################################
""""""""""
Piece square tables are used to evaluate the position of a piece on the board.
# The values are based on the position of the piece on the board.
"""""""""

# KNIGHT
knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0], 
                [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

# BISHOP
bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

# ROOK
rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

# QUEEN
queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

# PAWN
pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
                [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
                [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
                [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
                [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
                [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
                [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

# Dictionary to store the piece position scores
piece_position_scores = {"wN": knight_scores,
                        "bN": knight_scores[::-1],
                        "wB": bishop_scores,
                        "bB": bishop_scores[::-1],
                        "wQ": queen_scores,
                        "bQ": queen_scores[::-1],
                        "wR": rook_scores,
                        "bR": rook_scores[::-1],
                        "wp": pawn_scores,
                        "bp": pawn_scores[::-1]}



#######################################################################################################
##                                          AI LEVEL                                                 ##
#######################################################################################################

CHECKMATE = 1000   # White wins
STALEMATE = 0      # Draw
# DEPTH = 5          # How many moves ahead the AI should look: AI LEVEL (if too big it will take too long to calculate)



#######################################################################################################
##                                       FIND THE BEST MOVE                                          ##
#######################################################################################################

def findBestMove(game_state, valid_moves, return_queue, depthAux):
    global next_move
    next_move = None                                                                  # Next move to be made
    random.shuffle(valid_moves)                                                       # Randomize the valid moves
    findMoveNegaMaxAlphaBeta(game_state, valid_moves, depthAux, -CHECKMATE, CHECKMATE, 1 if game_state.white_to_move else -1, depthAux)
    return_queue.put(next_move)                                                       # Put the best move in the queue



#######################################################################################################
##                                      PIECE SQUARE TABLES                                         ##
#######################################################################################################

def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier, depthaux):
    global next_move
    if depth == 0:                                                                                                       # Base case
        return turn_multiplier * scoreBoard(game_state)                                                                  # Return the score
    # move ordering - implement later //TODO
    max_score = -CHECKMATE                                                                                               # Initialize the max score
    for move in valid_moves:                                                                                             # Loop through the valid moves
        game_state.makeMove(move, j=0)                                                                                   # Make the move
        next_moves = game_state.getValidMoves()                                                                          # Get the next moves
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier, depthaux)  # Recursively call the function
        if score > max_score:                                                                                            # Turn maximizing player
            max_score = score                                                                                            # Update the max score
            if depth == depthaux:                                                                                        # If we are at the root node
                next_move = move                                                                                         # Update the next move
        game_state.undoMove()                                                                                            # Undo the move
        if max_score > alpha:                                                                                            # Update the alpha value
            alpha = max_score                                                                                            # Update the alpha value
        if alpha >= beta:                                                                                                # Prune the tree
            break                                                                                                        # Break the loop
    return max_score                                                                                                     # Return the max score



#######################################################################################################
##                                          SCORE BOARD                                              ##
#######################################################################################################

def scoreBoard(game_state):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    if game_state.checkmate:                                                              # If the game is over
        if game_state.white_to_move:                                                      # If white wins
            return -CHECKMATE                                                             # Black wins
        else:
            return CHECKMATE                                                              # White wins
    elif game_state.stalemate:                                                            # If the game is a stalemate
        return STALEMATE
    score = 0                                                                             # Initialize the score
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):                                    # Loop through the board
            piece = game_state.board[row][col]                                           # Get the piece
            if piece != "--":                                                            # If the piece is not empty
                piece_position_score = 0                                                 # Initialize the piece position score
                if piece[1] != "K":                                                      # If the piece is not a king
                    piece_position_score = piece_position_scores[piece][row][col]        # Get the piece position score
                if piece[0] == "w":                                                      # If the piece is white
                    score += piece_score[piece[1]] + piece_position_score                # Update the score
                if piece[0] == "b":                                                      # If the piece is black
                    score -= piece_score[piece[1]] + piece_position_score                # Update the score

    return score



#######################################################################################################
##                                          RANDOM MOVES                                             ##
#######################################################################################################

def findRandomMove(valid_moves):
    """
    Picks and returns a random valid move.
    """
    return random.choice(valid_moves)        # Return a random move