"""
Main driver file.
Handling user input.
Displaying current GameStatus object.
"""
import pygame as p
import ChessEngine, ChessAI
import sys
from multiprocessing import Process, Queue

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # So that the pygame welcome message does not appear


BOARD_WIDTH = BOARD_HEIGHT = 512            # 600x600 pixels
MOVE_LOG_PANEL_WIDTH = 250                  # Width of the move log panel
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT        # Square size
DIMENSION = 8                               # 8x8 board
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION     # Size of each square
MAX_FPS = 15                                # For animations
IMAGES = {}                                 # Global dictionary of images

import tkinter as tk       # Imports tkinter module
from tkinter import ttk    # Imports ttk from tkinter




#######################################################################################################
##                                        LOAD IMAGES                                                ##
#######################################################################################################

def loadImages(): # Load images only once
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ'] # Piece names to load
    for piece in pieces: 
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE)) # Load and scale images



#######################################################################################################
##                                           GUI                                                     ##
#######################################################################################################
def GUI():
    # Crear la ventana principal
    ventana = tk.Tk() # CREA EL CUADRADO
    ventana.title("Configuración del Juego") # PONE EL TÍTULO
    ventana.geometry("600x300") # DA EL TAMAÑO DEL CUADRADO (ANCHO X ALTO)
    ventana.configure(bg="#f0f0f0")  # Color de fondo suave

    # Crear un contenedor para agrupar los elementos
    contenedor = ttk.Frame(ventana) # AÑADE EL WIDGET FRAME
    #contenedor.pack(padx=10, pady=10)
    contenedor.pack(fill=tk.BOTH, expand=True)

    # Estilo para los labels y opciones
    estilo = ttk.Style()
    estilo.configure("TLabel", font=("Helvetica", 12, "bold"), foreground="#4287f5")  # Azul principal
    estilo.configure("TMenubutton", font=("Helvetica", 11), background="#f0f0f0")  # Gris claro

    # Crear las opciones para cada lista desplegable
    opciones_jugadores1 = ["Jugador", "Jugador", "CPU"]
    opciones_jugadores2 = ["CPU", "Jugador", "CPU"]
    opciones_dificultad = [0, 0, 1, 2, 3, 4]

    # Crear las variables para almacenar las selecciones
    variable_blancas = tk.StringVar(ventana)
    #variable_blancas.set("Jugador")
    variable_negras = tk.StringVar(ventana)
    #variable_negras.set("CPU")
    variable_nivel = tk.IntVar(ventana)
    #variable_nivel.set(0)

    # Crear las listas desplegables con sus títulos
    ttk.Label(contenedor, text="Blancas:", style="TLabel").pack()
    def actualizar_blancas(valor):
        variable_blancas.set(valor)
    lista_desplegable_blancas = ttk.OptionMenu(contenedor, variable_blancas, *opciones_jugadores1, command=actualizar_blancas)
    lista_desplegable_blancas.pack()

    ttk.Label(contenedor, text="Negras:", style="TLabel").pack()
    def actualizar_negras(valor):
        variable_negras.set(valor)
    lista_desplegable_negras = ttk.OptionMenu(contenedor, variable_negras, *opciones_jugadores2, command=actualizar_negras)
    lista_desplegable_negras.pack()

    ttk.Label(contenedor, text="Nivel:", style="TLabel").pack()
    def actualizar_nivel(valor):
        variable_nivel.set(valor)
    lista_desplegable_nivel = ttk.OptionMenu(contenedor, variable_nivel, *opciones_dificultad, command=actualizar_nivel)
    lista_desplegable_nivel.pack()

    # Botón para cerrar la ventana
    boton_cerrar = ttk.Button(contenedor, text="Iniciar Juego", style="TButton",
                            command=lambda: [print(f"Blancas: {variable_blancas.get()}"), 
                                                                                print(f"Negras: {variable_negras.get()}"),
                                                                                print(f"Nivel: {variable_nivel.get()}"),
                                                                                ventana.destroy()])
    boton_cerrar.pack(pady=10)

    # Iniciar el bucle principal de la aplicación
    ventana.mainloop()

    return variable_blancas.get(), variable_negras.get(), variable_nivel.get()





#######################################################################################################
##                                        MAIN FUNCTION                                              ##
#######################################################################################################
def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    
    p.init()                                                                          # Initialize pygame module
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))   # Create a screen
    clock = p.time.Clock()                                                            # Create a clock object
    screen.fill(p.Color("white"))                                                     # Fill the screen with white color
    game_state = ChessEngine.GameState()                                              # Create a game state object
    valid_moves = game_state.getValidMoves()                                          # Get valid moves
    move_made = False                                                                 # Flag variable for when a move is made
    animate = False                                                                   # Flag variable for when we should animate a move
    loadImages()                                                                      # Do this only once before while loop
    running = True                                                                    # Flag variable to keep our game loop running
    square_selected = ()                                                              # No square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = []                                                                # This will keep track of player clicks, two tuples
    game_over = False                                                                 # Flag variable to keep track of if the game is over
    ai_thinking = False                                                               # Flag variable to keep track of if AI is thinking
    move_undone = False                                                               # Flag variable to keep track of if a move is undone
    move_finder_process = None                                                        # Variable to keep track of the process of finding the best move
    move_log_font = p.font.SysFont("Arial", 18, False, False)                         # Font for move log
    player_one = True                                                                 # If a human is playing white, then this will be True, else False
    player_two = False                                                                # If a hyman is playing white, then this will be True, else False

    while running: 
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two) # Check if it is human's turn
        for e in p.event.get(): 
            if e.type == p.QUIT:                                                                      # IF USER CLICKS THE CLOSE BUTTON
                p.quit()                                                                                 # Quit the game
                sys.exit()                                                                               # Exit the program
            elif e.type == p.MOUSEBUTTONDOWN:                                                         # IF USER CLICKS THE MOUSE
                if not game_over:                                                                        # IF GAME IS NOT OVER
                    location = p.mouse.get_pos()                                                             # (x, y) location of the mouse
                    col = location[0] // SQUARE_SIZE                                                         # Get the column
                    row = location[1] // SQUARE_SIZE                                                         # Get the row
                    if square_selected == (row, col) or col >= 8:                                            # IF USER CLICKS THE SAME SQUARE TWICE OR CLICKS OUTSIDE THE BOARD
                        square_selected = ()                                                                    # Deselect 
                        player_clicks = []                                                                      # Clear player clicks
                    else:
                        square_selected = (row, col)                                                            # Set the selected square
                        player_clicks.append(square_selected)                                                   # Append for both 1st and 2nd click
                    if len(player_clicks) == 2 and human_turn:                                                  # AFTER 2ND CLICK
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)           # Create a move object
                        for i in range(len(valid_moves)):                                                       # Check if the move is valid
                            if move == valid_moves[i]:                                                          # IIF IT IS VALID
                                game_state.makeMove(valid_moves[i], j=1)                                                 # Make the move
                                move_made = True                                                                    # Move is made
                                animate = True                                                                      # Animate the move
                                square_selected = ()                                                                # Reset the square selected
                                player_clicks = []                                                                  # Reset the player clicks
                        if not move_made:                                                                       # IF MOVE IS NOT MADE
                            player_clicks = [square_selected]                                                       # Reset the player clicks

            elif e.type == p.KEYDOWN:                                                                 # IF USER PRESSES A KEY
                if e.key == p.K_z:                                                                       # Undo when 'z' is pressed 
                    game_state.undoMove()                                                                   # Undo the move
                    move_made = True                                                                        # Move is made
                    animate = False                                                                         # Animate the move
                    game_over = False                                                                       # Game is not over
                    if ai_thinking:                                                                         # IF AI IS THINKING
                        move_finder_process.terminate()                                                         # Terminate the process
                        ai_thinking = False                                                                     # AI is not thinking
                    move_undone = True                                                                      # Move is undone
                if e.key == p.K_r:                                                                      # Reset the game when 'r' is pressed 
                    game_state = ChessEngine.GameState()                                                   # Reset the game state
                    valid_moves = game_state.getValidMoves()                                               # Get valid moves
                    square_selected = ()                                                                   # Reset the square selected
                    player_clicks = []                                                                     # Reset the player clicks
                    move_made = False                                                                      # Move is not made
                    animate = False                                                                        # Animate the move 
                    game_over = False                                                                      # Game is not over
                    if ai_thinking:                                                                        # IF AI IS THINKING
                        move_finder_process.terminate()                                                       # Terminate the process
                        ai_thinking = False                                                                   # AI is not thinking
                    move_undone = True                                                                     # Move is undone

        # AI move finder
        if not game_over and not human_turn and not move_undone:                                 # IF GAME IS NOT OVER AND IT IS NOT HUMAN'S TURN AND MOVE IS NOT UNDONE
            if not ai_thinking:                                                                     # IF AI IS NOT THINKING
                ai_thinking = True                                                                      # AI is thinking
                return_queue = Queue()                                                                  # Used to pass data between threads
                move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, valid_moves, return_queue)) # Create a process
                move_finder_process.start()                                                             # Start the process

            if not move_finder_process.is_alive():                                                 # IF MOVE FINDER PROCESS IS NOT ALIVE
                ai_move = return_queue.get()                                                            # Get the best move from the queue
                if ai_move is None:                                                                     # IF AI MOVE IS NONE
                    ai_move = ChessAI.findRandomMove(valid_moves)                                         # Find a random move
                game_state.makeMove(ai_move)                                                            # Make the move
                move_made = True                                                                        # Move is made
                animate = True                                                                          # Animate the move
                ai_thinking = False                                                                     # AI is not thinking

        if move_made:                                                                           # IF MOVE IS MADE
            if animate:                                                                            # IF ANIMATE IS TRUE
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)                 # Animate the move
            valid_moves = game_state.getValidMoves()                                               # Get valid moves
            move_made = False                                                                      # Reset the move made flag
            animate = False                                                                        # Reset the animate flag
            move_undone = False                                                                    # Reset the move undone flag

        drawGameState(screen, game_state, valid_moves, square_selected)                         # Draw the game state

        if not game_over:                                                                      # IF GAME IS NOT OVER
            drawMoveLog(screen, game_state, move_log_font)                                         # Draw the move log

        if game_state.checkmate:                                                              # IF GAME IS CHECKMATE
            game_over = True                                                                     # Game is over
            if game_state.white_to_move:                                                         # IF WHITE TO MOVE
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif game_state.stalemate:                                                            # IF GAME IS STALEMATE
            game_over = True                                                                     # Game is over
            drawEndGameText(screen, "Stalemate")

        clock.tick(MAX_FPS)                                                                   # Set the maximum frames per second
        p.display.flip()                                                                      # Update the display



#######################################################################################################
##                                       DRAW GAME STATE                                             ##
#######################################################################################################

def drawGameState(screen, game_state, valid_moves, square_selected):    # Draw the game state
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)                                                   # Draw squares on the board
    highlightSquares(screen, game_state, valid_moves, square_selected)  # Highlight squares
    drawPieces(screen, game_state.board)                                # Draw pieces on top of those squares



#######################################################################################################
##                                        DRAW THE BOARD                                             ##
#######################################################################################################

def drawBoard(screen): 
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors                                                                                                     # Global variable
    colors = [p.Color("white"), p.Color("gray")]                                                                      # Colors for the board
    for row in range(DIMENSION): 
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]                                                                      # Color of the square
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))     # Draw the square



#######################################################################################################
##                                      HIGHLIGHTS SQUARES                                           ##
#######################################################################################################

def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.move_log)) > 0:                                                       # Check if there is a move made
        last_move = game_state.move_log[-1]                                                  # Get the last move
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))                                            # Create a surface
        s.set_alpha(100)                                                                     # Set the transparency value
        s.fill(p.Color('green'))                                                             # Fill the surface with green color
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))   # Blit the surface
    if square_selected != ():                                                                # Check if a square is selected
        row, col = square_selected                                                           # Get the row and column
        if game_state.board[row][col][0] == (
                'w' if game_state.white_to_move else 'b'):                                   # Square_selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))                                        # Create a surface
            s.set_alpha(100)                                                                 # Transparency value 0 -> transparent, 255 -> opaque
            s.fill(p.Color('blue'))                                                          # Fill the surface with blue color
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))                           # Blit the surface
            # highlight moves from that square
            s.fill(p.Color('yellow'))                                                        # Fill the surface with yellow color
            for move in valid_moves: 
                if move.start_row == row and move.start_col == col:                          # Check if the move is valid
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE)) # Blit the surface



#######################################################################################################
##                                        DRAW PIECES                                             ##
#######################################################################################################

def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



#######################################################################################################
##                                       DRAW MOVE LOG                                               ##
#######################################################################################################

def drawMoveLog(screen, game_state, font):
    """
    Draws the move log.

    """
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT) # Create a rectangle
    p.draw.rect(screen, p.Color('black'), move_log_rect)                                # Draw the rectangle
    move_log = game_state.move_log                                                      # Get the move log
    move_texts = []                                                                     # List to store the move texts
    for i in range(0, len(move_log), 2):                                                # Loop through the move log
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "                   # Create a move string 
        if i + 1 < len(move_log):                                                       # Check if there is a next move
            move_string += str(move_log[i + 1]) + "  "                                  # Add the next move
        move_texts.append(move_string)                                                  # Append the move string

    moves_per_row = 3                                                                   # Moves per row
    padding = 5                                                                         # Padding
    line_spacing = 2                                                                    # Line spacing
    text_y = padding                                                                    # Text y
    for i in range(0, len(move_texts), moves_per_row):                                  # Loop through the move texts
        text = "" 
        for j in range(moves_per_row):                                                  # Loop through the moves per row
            if i + j < len(move_texts):                                                 # Check if there is a move
                text += move_texts[i + j]                                               # Add the move

        text_object = font.render(text, True, p.Color('white'))                         # Render the text
        text_location = move_log_rect.move(padding, text_y)                             # Move the text  
        screen.blit(text_object, text_location)                                         # Blit the text   
        text_y += text_object.get_height() + line_spacing                               # Update the text y



#######################################################################################################
##                                     DRAW END GAME TEXT                                            ##
#######################################################################################################

def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)                                                           # Font for the text
    text_object = font.render(text, False, p.Color("gray"))                                                       # Render the text
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                BOARD_HEIGHT / 2 - text_object.get_height() / 2)  # Move the text
    screen.blit(text_object, text_location)                                                                       # Blit the text
    text_object = font.render(text, False, p.Color('black'))                                                      # Render the text
    screen.blit(text_object, text_location.move(2, 2))                                                            # Blit the text



#######################################################################################################
##                                        ANIMATE MOVE                                               ##
#######################################################################################################

def animateMove(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_row = move.end_row - move.start_row                                                                                 # Change in row
    d_col = move.end_col - move.start_col                                                                                 # Change in column
    frames_per_square = 10                                                                                                # Frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square                                                           # Total frames to move
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)           # Get the row and column
        drawBoard(screen)                                                                                                 # Draw the board
        drawPieces(screen, board)                                                                                         # Draw the pieces
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]                                                                 # Color of the square
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)             # Rectangle for the square
        p.draw.rect(screen, color, end_square)                                                                            # Draw the rectangle
        # draw captured piece onto rectangle
        if move.piece_captured != '--':                                                                                   # If a piece is captured
            if move.is_enpassant_move:                                                                                    # If it is an enpassant move
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1                   # Get the row
                end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)    # Rectangle for the square
            screen.blit(IMAGES[move.piece_captured], end_square)                                                          # Blit the image
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))     # Blit the image
        p.display.flip()                                                                                                  # Update the display
        clock.tick(60)                                                                                                    # Set the frames per second



#######################################################################################################
##                                                CALLS                                              ##
#######################################################################################################

if __name__ == "__main__": # Call the main function
    i =+1
    if i == 1:
        P1E, P2E, nivel = GUI()
    
    main()
