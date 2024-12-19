"""
Main driver file.
Handling user input.
Displaying current GameStatus object.
"""

import tkinter as tk # Importa el módulo tkinter y le asigna el alias tk
from tkinter import ttk # importa el submódulo ttk desde tkinter
import time
from multiprocessing import Process, Queue
from os import environ
import pygame as p
import ChessEngine
import ChessAI

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # Para que no salga todo el rato el cartel

BOARD_WIDTH = BOARD_HEIGHT = 800 #512 # Tamaño del tablero (se ajusta solo las piezas)
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def GUI():
    """
    Crea una GUI en la que se puede elegir:
        - Jugador blancas: Usuario/CPU
        - Jugador negras: Usuario/CPU
        - Dificultad: 0-4
        - Tiempo de juego
    """
    # Crear la ventana principal
    ventana = tk.Tk() # CREA EL CUADRADO
    ventana.title("Configuración del Juego") # PONE EL TÍTULO
    ventana.geometry("600x350") # DA EL TAMAÑO DEL CUADRADO (ANCHO X ALTO)
    ventana.configure(bg="#f0f0f0")  # Color de fondo suave

    # Crear un contenedor para agrupar los elementos
    contenedor = ttk.Frame(ventana) # AÑADE EL WIDGET FRAME
    contenedor.pack(fill=tk.BOTH, expand=True)

    # Estilo para los labels y opciones
    estilo = ttk.Style()
    estilo.configure("TLabel", font=("Helvetica", 12, "bold"), foreground="#4287f5")  # Azul
    estilo.configure("TMenubutton", font=("Helvetica", 11), background="#f0f0f0")  # Gris claro

    # Crear las opciones para cada lista desplegable
    opciones_jugadores1 = ["Jugador", "Jugador", "CPU"]
    opciones_jugadores2 = ["CPU", "Jugador", "CPU"]
    opciones_dificultad = [0, 0, 1, 2, 3, 4]

    # Crear las variables para almacenar las selecciones
    var_blancas = tk.StringVar(ventana)
    var_negras = tk.StringVar(ventana)
    var_nivel = tk.IntVar(ventana)
    var_tiempo = tk.StringVar(ventana)

    # Crear las listas desplegables con sus títulos
    ttk.Label(contenedor, text="Blancas:", style="TLabel").pack()
    def actualizar_blancas(valor):
        var_blancas.set(valor)
    lista_desplegable_blancas = ttk.OptionMenu(contenedor, var_blancas,
                                               *opciones_jugadores1, command=actualizar_blancas)
    lista_desplegable_blancas.pack()

    ttk.Label(contenedor, text="Negras:", style="TLabel").pack()
    def actualizar_negras(valor):
        var_negras.set(valor)
    lista_desplegable_negras = ttk.OptionMenu(contenedor, var_negras,
                                              *opciones_jugadores2, command=actualizar_negras)
    lista_desplegable_negras.pack()

    ttk.Label(contenedor, text="Nivel:", style="TLabel").pack()
    def actualizar_nivel(valor):
        var_nivel.set(valor)
    lista_desplegable_nivel = ttk.OptionMenu(contenedor, var_nivel,
                                             *opciones_dificultad, command=actualizar_nivel)
    lista_desplegable_nivel.pack()

    ttk.Label(contenedor, text="Tiempo (mins):", style="TLabel").pack()
    entrada_tiempo = ttk.Entry(contenedor, textvariable=var_tiempo)
    entrada_tiempo.pack()
    entrada_tiempo.insert(0, "3") # HACERLO A PRUEBA DE TONTOS

    # Botón para cerrar la ventana
    boton_cerrar = ttk.Button(contenedor, text="Iniciar Juego", style="TButton",
                             command=lambda: [print(f"Blancas: {var_blancas.get()}"),
                                                        print(f"Negras: {var_negras.get()}"),
                                                        print(f"Nivel: {var_nivel.get()}"),
                                                        ventana.destroy()])
    boton_cerrar.pack(pady=10)

    # Iniciar el bucle principal de la aplicación
    ventana.mainloop()

    return var_blancas.get(), var_negras.get(), var_nivel.get(), var_tiempo.get()


def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        # ajusta el tamaño de las piezas al tamaño del tablero
        IMAGES[piece] = p.transform.scale(p.image.load("My milestones\Milestone 7\images/"+piece+".png"),
                                            (SQUARE_SIZE,SQUARE_SIZE))

def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    p_1 = bool(p1_e == "Jugador")

    p_2 = bool(p2_e == "Jugador")

    p.init() # pylint: disable=no-member
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    #screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
    valid_moves = game_state.getValidMoves()
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move
    loadImages()  # do this only once before while loop
    running = True
    square_selected = ()
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)
    player_one = p_1  # if a human is playing white, then this will be True, else False
    player_two = p_2  # if a human is playing black, then this will be True, else False

    # Inicializar la fuente para los temporizadores
    font = p.font.Font(None, 30)


    # Variables del temporizador (AHORA CON TIEMPO DE INICIO INDIVIDUAL)
    time_limit = float(tiempo) * 60  # 30 segundos

    # Variables del temporizador 1 (Jugador Blanco)
    time_left1 = time_limit
    timer_active1 = False

    # Variables del temporizador 2 (Jugador Negro)
    time_left2 = time_limit
    timer_active2 = False

    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        for e in p.event.get(): # pylint: disable=invalid-name
            if e.type == p.QUIT: # pylint: disable=no-member
                running = False
                break
            # mouse handler
            if e.type == p.MOUSEBUTTONDOWN: # pylint: disable=no-member
                if not game_over:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if square_selected == (row, col) or col >= 8:
                        square_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)  # append for both 1st and 2nd click
                    if len(player_clicks) == 2 and human_turn:  # after 2nd click
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1],game_state.board)
                        for move_option in valid_moves:
                            if move == move_option:
                                game_state.makeMove(move_option, j=1)
                                move_made = True
                                animate = True
                                square_selected = ()  # reset user clicks
                                player_clicks = []
                            if not move_made:
                                player_clicks = [square_selected]

            # key handler
            elif e.type == p.KEYDOWN: # pylint: disable=no-member
                if e.key == p.K_z:  # pylint: disable=no-member
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == p.K_r:  # pylint: disable=no-member
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

        # --- Lógica CRUCIAL para el manejo de turnos y temporizadores ---
        if not game_over:
            if game_state.white_to_move:  # Turno del blanco
                if not timer_active1:  # Si no estaba activo, se inicia el tiempo
                    start_time1 = time.time() # Se guarda el tiempo de inicio del turno
                    timer_active1 = True
                    timer_active2 = False
            else:  # Turno del negro
                if not timer_active2:  # Si no estaba activo, se inicia el tiempo
                    start_time2 = time.time() # Se guarda el tiempo de inicio del turno
                    timer_active2 = True
                    timer_active1 = False

        # AI move finder
        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()  # used to pass data between threads
                move_finder_process = Process(target=ChessAI.findBestMove,
                                        args=(game_state, valid_moves, return_queue, nivel))
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

        # Actualizar los temporizadores (AHORA CON LA LÓGICA CORRECTA)
        if timer_active1 and not game_over:
            elapsed_time = time.time() - start_time1 # Tiempo transcurrido desde el inicio del turno
            time_left1 -= elapsed_time # Se resta el tiempo transcurrido al tiempo restante
            time_left1 = max(0, time_left1) # Se asegura de que no sea negativo
            start_time1 = time.time() # Se actualiza el tiempo de inicio para la siguiente iteración

            if time_left1 <= 0:
                game_over = True
                winner = "Black"

        if timer_active2 and not game_over:
            elapsed_time = time.time() - start_time2
            time_left2 -= elapsed_time
            time_left2 = max(0, time_left2)
            start_time2 = time.time()

            if time_left2 <= 0:
                game_over = True
                winner = "White"

        if not game_over:  # Solo limpiar la pantalla si el juego NO ha terminado
            screen.fill(p.Color("white"))

        # Formatear y renderizar los temporizadores (sin cambios aquí)
        minutes1 = int(time_left1 // 60)
        seconds1 = int(time_left1 % 60)
        time_str1 = f"{minutes1:02}:{seconds1:02}"
        time_text1 = font.render(time_str1, True, p.Color("black"))
        text_rect1 = time_text1.get_rect()
        text_rect1.bottomleft = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - 200, BOARD_HEIGHT - 10)

        minutes2 = int(time_left2 // 60)
        seconds2 = int(time_left2 % 60)
        time_str2 = f"{minutes2:02}:{seconds2:02}"
        time_text2 = font.render(time_str2, True, p.Color("black"))
        text_rect2 = time_text2.get_rect()
        text_rect2.bottomright = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - 10, BOARD_HEIGHT - 10)


        #screen.fill(p.Color("white"))

        drawGameState(screen, game_state, valid_moves, square_selected)

        # Dibujar el temporizador
        screen.blit(time_text1, text_rect1) # Dibujar temporizador 1
        screen.blit(time_text2, text_rect2) # Dibujar temporizador 2


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
        elif game_over and "winner" in locals(): # Se añade esta condición
            drawEndGameText(screen, f"{winner} wins by time")


        p.display.flip()
        clock.tick(MAX_FPS)


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
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE,
                                row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

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
        # square_selected is a piece that can be moved
        if game_state.board[row][col][0] == (
                'w' if game_state.white_to_move else 'b'):  
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
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE,
                                        row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawMoveLog(screen, game_state, font):
    """
    Draws the move log.

    """
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT-50)
    p.draw.rect(screen, p.Color('black'), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i_3 in range(0, len(move_log), 2):
        move_string = str(i_3 // 2 + 1) + '. ' + str(move_log[i_3]) + " "
        if i_3 + 1 < len(move_log):
            move_string += str(move_log[i_3 + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 2
    padding = 5
    line_spacing = 2
    text_y = padding
    for i_4 in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i_4 + j < len(move_texts):
                text += move_texts[i_4 + j]

        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing

def drawEndGameText(screen, text):
    """
    Pinta el cartel de final de partida, por el motivo que haya sido
    """
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0,
                            BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2-text_object.get_width() /2,
                                                        BOARD_HEIGHT/2-text_object.get_height() / 2)
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
        row,col=(move.start_row+d_row*frame/frame_count,move.start_col+d_col*frame/frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square=p.Rect(move.end_col*SQUARE_SIZE,move.end_row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0]== 'b' else move.end_row-1
                end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE,
                                    SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE,
                                            row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    i =+1
    if i == 1:
        p1_e, p2_e, nivel, tiempo = GUI()

    main()
