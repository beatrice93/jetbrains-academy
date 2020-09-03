"""
A game of Tic-Tac Toe. Project from hyperskill.org.

Learning objectives:
    - Basic: control statements, array manipulations, recursions;
    - Minimax implementation;
Suggested improvements:
    - Store board in a list to clean up indices (maybe this would make it less legible though);
    - Speed up minimax implementation;
Wisdom learned:
    - CHECK YOUR O'S ARE O'S AND NOT 0'S
"""

import random as rd

size = 3


def display_game(board):
    print("---------")
    for i in range(size):
        print("| " + ' '.join(board[i]) + " |")
    print("---------")


def scan(board, cells):
    """
    Scans a list of tuples for winning move. 
    Returns (A, b) where A is "X" or "O" and b is "win" if all cells are occupied by A, 
    or (i, j) if (i, j) is the only empty cell in the list. 
    """
    
    if board[cells[0][0]][cells[0][1]] != ' ':
        current_player = board[cells[0][0]][cells[0][1]]
    elif board[cells[1][0]][cells[1][1]] != ' ':
        current_player = board[cells[1][0]][cells[1][1]]
    else:
        return None
    best_move = None
    occupied_spots = 0
    for (i, j) in cells:
        if board[i][j] == current_player:
            occupied_spots += 1
        elif board[i][j] == ' ':
            best_move = (i, j)
        else:
            return None
    if occupied_spots == size - 1:
        return current_player, best_move
    elif occupied_spots == size:
        return current_player, "win"
    else:
        return None


def check_state(board):
    """
    Compute the game state.
    Returns a dictionary {"X": (a,b), "O": (c,d), "win": "A"}
    where (a,b) is a winning move for X (if applicable),
    (c, d) winning move for O (if applicable)
    and "A" is the player who won (if applicable)
    """

    game_state = {"X": False, "O": False, "win": False}
    
    for i in range(size):
        check_row = scan(board, [(i, j) for j in range(size)])
        if check_row:
            if check_row[1] == "win":
                game_state["win"] = check_row[0]
                return game_state
            else:
                game_state[check_row[0]] = check_row[1]
    
    for j in range(size):
        check_col = scan(board, [(i, j) for i in range(size)])
        if check_col:
            if check_col[1] == "win":
                game_state["win"] = check_col[0]
                return game_state
            else:
                game_state[check_col[0]] = check_col[1]
    
    check_diag = scan(board, [(i, i) for i in range(size)])
    if check_diag:
        if check_diag[1] == "win":
            game_state["win"] = check_diag[0]
            return game_state
        else:
            game_state[check_diag[0]] = check_diag[1]
            
    check_adiag = scan(board, [(i, size - i - 1) for i in range(size)])
    if check_adiag:
        if check_adiag[1] == "win":
            game_state["win"] = check_adiag[0]
            return game_state
        else:
            game_state[check_adiag[0]] = check_adiag[1]
            
    return game_state


def minimax(board, current, ai):
    """
    Finds winning move using minimax algorithm
    parameters:
        - board: current board as an array
        - free_cells: list of tuples
        - current: player for this move
        - ai: who the ai is playing
    """
    free_cells = set([(i, j) for i in range(size) for j in range(size) if board[i][j] == ' '])

    if check_state(board)["win"] == ai:
        return 10, 0, 0
    elif check_state(board)["win"]:
        return -10, 0, 0
    elif not free_cells:
        return 0, 0, 0

    if current == ai:
        move_score = -100
        move_i, move_j = 0, 0
        for i in range(size):
            for j in range(size):
                if board[i][j] == ' ':
                    board[i][j] = current
                    minmax = minimax(board, "X" if current == "O" else "O", ai)[0]
                    if minmax > move_score:
                        move_score = minmax
                        move_i, move_j = i, j
                    board[i][j] = ' '

    else:
        move_score = 100
        move_i, move_j = 0, 0
        for i in range(size):
            for j in range(size):
                if board[i][j] == ' ':
                    board[i][j] = current
                    minmax = minimax(board, "X" if current == "O" else "O", ai)[0]
                    if minmax < move_score:
                        move_score = minmax
                        move_i, move_j = i, j
                    board[i][j] = ' '

    return move_score, move_i, move_j


menu_choice = ""
while menu_choice != "exit":

    valid_choice = False
    while not valid_choice:
        menu = input("\nInput command:").split()
        if menu == ["exit"]:
            valid_choice = True
            menu_choice = "exit"
        elif len(menu) == 3 and menu[0] in ["start", "exit"] and all(
                [menu[i] in ["user", "easy", "medium", "hard"] for i in range(1, 3)]):
            menu_choice, player1, player2 = menu
            valid_choice = True
        else:
            print("Bad parameters!")

    if menu_choice == "start":

        game = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        empty_cells = {(i, j) for i in range(size) for j in range(size)}
        turn = 1

        player_move = [player2, player1]  # switched because turn starts at 1

        while not check_state(game)["win"] and any(empty_cells):
            display_game(game)

            if player_move[turn % 2] == "user":
                valid_move = False
                while not valid_move:

                    move = input("Enter the coordinates: ").split()

                    if all(coord in [str(n) for n in range(1, size + 1)] for coord in move):
                        if game[size - int(move[1])][int(move[0]) - 1] in ["X", "O"]:
                            print("This cell is occupied! Choose another one!")
                        else:
                            game[size - int(move[1])][int(move[0]) - 1] = "X" if turn % 2 else "O"
                            empty_cells.remove((size - int(move[1]), int(move[0]) - 1))
                            valid_move = True
                            turn += 1

                    elif all(coord in [str(n) for n in range(10)] for coord in ''.join(move)):
                        print("Coordinates should be from 1 to {}!".format(size))
                    else:
                        print("You should enter numbers!")

            elif player_move[turn % 2] == "easy":
                print('Making move level "easy"')
                move = rd.choice(list(empty_cells))
                game[move[0]][move[1]] = "X" if turn % 2 else "O"
                empty_cells.remove((move[0], move[1]))
                turn += 1

            elif player_move[turn % 2] == "medium":
                print('Making move level "medium"')
                game_state = check_state(game)
                if turn % 2:
                    if game_state["X"]:
                        move = game_state["X"]
                    elif game_state["O"]:
                        move = game_state["O"]
                    else:
                        move = rd.choice(list(empty_cells))
                    game[move[0]][move[1]] = "X"

                else:
                    if game_state["O"]:
                        move = game_state["O"]
                    elif game_state["X"]:
                        move = game_state["X"]
                    else:
                        move = rd.choice(list(empty_cells))
                    game[move[0]][move[1]] = "O"

                empty_cells.remove((move[0], move[1]))
                turn += 1

            else:
                print('Making move level "hard"')
                if turn == 1:
                    game[0][0] = "X"
                    empty_cells.remove((0, 0))
                else:
                    ai = "X" if turn % 2 else "O"
                    move = (minimax(game, ai, ai)[1], minimax(game, ai, ai)[2])
                    if turn % 2:
                        game[move[0]][move[1]] = "X"
                    else:
                        game[move[0]][move[1]] = "O"
                    empty_cells.remove((move[0], move[1]))
                turn += 1

        display_game(game)

        if check_state(game)["win"]:
            print(check_state(game)["win"] + " wins")
        else:
            print("Draw")
