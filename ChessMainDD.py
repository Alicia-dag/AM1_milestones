"""
Main driver file.
Handling user input.
Displaying current GameStatus object.
"""
import pygame as p
import ChessEngine, ChessAI
import sys
from multiprocessing import Process, Queue
import threading

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # Para que no salga todo el rato el cartel de "Hello from the pygame community"

BOARD_WIDTH = BOARD_HEIGHT = 800 #512 # Tamaño del tablero (se ajusta solo las piezas)
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

import tkinter as tk # Importa el módulo tkinter y le asigna el alias tk
from tkinter import ttk # importa el submódulo ttk desde tkinter

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


def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE)) # ajusta el tamaño de las piezas al tamaño del tablero

def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """    
    if P1E == "Jugador":
        P1 = True
    else:
        P1 = False

    if P2E=="Jugador":
        P2 = True
    else:
        P2 = False

    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
    valid_moves = game_state.getValidMoves()
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move
    loadImages()  # do this only once before while loop
    running = True
    square_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)
    player_one = P1  # if a human is playing white, then this will be True, else False
    player_two = P2  # if a human is playing black, then this will be True, else False

    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                        square_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)  # append for both 1st and 2nd click
                    if len(player_clicks) == 2 and human_turn:  # after 2nd click
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i], j=1)
                                move_made = True
                                animate = True
                                square_selected = ()  # reset user clicks
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == p.K_r:  # reset the game when 'r' is pressed
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

        # AI move finder
        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()  # used to pass data between threads
                move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, valid_moves, return_queue, nivel))
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:
                    ai_move = ChessAI.findRandomMove(valid_moves)
                game_state.makeMove(ai_move, j=0)
                move_made = True
                animate = True
                ai_thinking = False

        if move_made:
            if animate:
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False
            move_undone = False

        drawGameState(screen, game_state, valid_moves, square_selected)

        if not game_over:
            drawMoveLog(screen, game_state, move_log_font)

        if game_state.checkmate:
            game_over = True
            if game_state.white_to_move:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif game_state.stalemate:
            game_over = True
            drawEndGameText(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, game_state, valid_moves, square_selected):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares

def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == (
                'w' if game_state.white_to_move else 'b'):  # square_selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))

def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawMoveLog(screen, game_state, font):
    """
    Draws the move log.

    """
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 1
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing

def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))

def animateMove(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)






class CountdownClock:
    def __init__(self, root, countdown_time): # Constructor de la clase
        self.root = root
        self.time_left = countdown_time  # Tiempo inicial en segundos
        self.running = True  # Indica si el reloj está funcionando

        # Configuración de la interfaz
        self.label = tk.Label(root, text=self.format_time(self.time_left), font=("Helvetica", 48)) 
        self.label.pack(pady=20)

        self.button = tk.Button(root, text="Detener", command=self.toggle)
        self.button.pack(pady=10)

        self.update_clock()

    def format_time(self, seconds): # Pasa de segundos a minutos y segundos
        """Formatea los segundos como MM:SS."""
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"

    def update_clock(self): # Actualiza el reloj
        """Actualiza el temporizador cada segundo."""
        if self.running and self.time_left > 0: # Si el temporizador está en funcionamiento y no ha terminado
            self.time_left -= 1 # Resta 1 segundo
            self.label.config(text=self.format_time(self.time_left)) # Actualiza la etiqueta con el tiempo restante
            self.root.after(1000, self.update_clock)  # Llama a esta función en 1 segundo
        elif self.time_left == 0: # Si el tiempo ha terminado
            self.label.config(text="¡Tiempo terminado!") # Muestra un mensaje

    def toggle(self): # Activa o pausa el temporizador
        """Activa o pausa el temporizador."""
        self.running = not self.running # Cambia el estado del temporizador
        if self.running:  # Si se reanuda, actualizar el reloj
            self.update_clock() # Actualiza el reloj

            # Ensure the countdown clock GUI appears in front of the chess board GUI
            def showCountdownClock(): # Muestra el reloj de cuenta atrás
                root = tk.Tk() # Crea una nueva ventana
                root.title("Reloj de Cuenta Atrás") # Pone el título de la ventana
                countdown_time = 60  # Tiempo inicial en segundos (por ejemplo, 1 minuto)
                app = CountdownClock(root, countdown_time)
                root.mainloop()

            # Start the countdown clock GUI in a separate thread
            clock_thread = threading.Thread(target=showCountdownClock)
            clock_thread.start()

if __name__ == "__main__":
    i =+1
    if i == 1:
        P1E, P2E, nivel = GUI()

        # Start the main game loop in a separate thread
        game_thread = threading.Thread(target=main)
        game_thread.start()
    root = tk.Tk()
    root.title("Reloj de Cuenta Atrás")
    countdown_time = 60  # Tiempo inicial en segundos (por ejemplo, 1 minuto)

    app = CountdownClock(root, countdown_time)
    root.mainloop()
    
    main()
