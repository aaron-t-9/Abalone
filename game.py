import math
import random

from tkinter import messagebox
from ai.ai import *
from utils.settings import *
from utils.converter import Converter
from utils.move import Move
from copy import deepcopy


class GameBoard(tk.Tk):
    """
    Encapsulates the methods related to drawing, initializing, and creating the game board for Abalone.
    """

    def __init__(self):
        super().__init__()

        # default font and turn_color
        self.font = "Montserrat", 15
        self.font_color = "White"

        # default background turn_color
        self.bg = "#303b41"

        self.title("Abalone (not the snail) - G5")
        self.width = 700
        self.height = 500
        self.canvas = Canvas(self, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)
        self.board_width = 500
        self.hexes_per_side = 5
        self.hexes_across = 2 * self.hexes_per_side - 1
        self.hex_size = self.board_width // self.hexes_across
        self.spot_radius = 25 * self.board_width / 550
        self.piece_radius = 26 * self.board_width / 550
        self.selection_radius = 26 * self.board_width / 550
        self.selection_redraw_radius = 23 * self.board_width / 550
        self.turn_count_black = 0
        self.turn_count_white = 0
        self.turn = "black"  # black always goes first
        self.game_over = False
        self.selected_pieces = {}
        self.last_hex = None
        # self.white_timer = 0
        # self.black_timer = 0
        # self.white_timer = None
        # self.black_timer = None
        self.black_total_time = 0
        self.white_total_time = 0
        self.white_timer_box = None
        self.black_timer_box = None
        self.white_moves_box = None
        self.black_moves_box = None
        self.white_move_count = None
        self.black_move_count = None
        self.white_pieces = None
        self.black_pieces = None
        self.settings = None
        self.settings_selections = {'turn_color': 1, 'mode_p1': "Human", 'mode_p2': "Human", 'config': 0, 'turns': 30,
                                    'time1': 5, 'time2': 5}
        self.spot_coords = {}
        self.board_screen_pos = None
        self.game_board = None
        self.current_move_timer_label = None

        # ----- AI ----- #
        self.Minimax = Minimax()
        self.ai_moved_pieces = []
        self.human_vs_human = False

        # ----- Piece Movement ----- #
        self.Move = Move()  # initializes the Move object
        self.adjacent_spaces = set()
        self.possible_inline_moves = set()
        self.possible_sidestep_moves = []
        self.selected_pieces = []
        self.selected_pieces_xy_coords = []
        self.num_pieces_selected = 0
        self.sumito_chain = []  # stores the chain of pieces to be sumito, in order
        self.dir_tuple_sumito = ()  # stores the vector of direction for the sumito chain
        self.first_piece_selection = None  # stores the index of piece adjacent to first piece in sumito chain
        self.latest_human_move = ()  # stores the latest human move
        self.human_start = time.perf_counter()

        # ----- Undo Moves ----- #
        self.previous_board_states = []

    @staticmethod
    def get_row_key(row: int, offset=0) -> str:
        """
        Generates the key used for the game_board dictionary for denoting the rows of the game board. An offset
        may be specified as the index starts at 0, otherwise the offset is default at 0.
        :param row: an int
        :param offset: an int
        :return: a string
        """
        return "row" + str(row + offset)

    @staticmethod
    def print_selected_piece_coord(row, col):
        """
        Translates the coordinates for the selected game piece according to the I-A and 1-9 game board
        coordinate system, and prints it to the terminal.
        :param row: an int
        :param col: an int
        """
        coords = Converter.internal_notation_to_external(row, col)
        row_coord = coords[0]
        col_coord = coords[1]

        print(f"Selected piece at: {row_coord}{col_coord}")

    def click_event_listener_engine(self, event):
        """
        Handles the user's on-screen click event, and determines if the player has clicked on a game piece. If a game
        piece has been clicked, it is highlighted and the selected game piece is colored green.
        :param event: an Event object containing various data attributes including the x and y coords of the click event
        """
        DEBUG_PRINT_STATEMENTS = False  # setting to True enables print statements that contain additional Click & Piece information
        RANGE = 20
        # Timer check for human player
        if self.turn == "black":
            turn_timer = self.settings_selections['time1']
        else:
            turn_timer = self.settings_selections['time2']
        time_taken = time.perf_counter() - self.human_start
        if time_taken > turn_timer:
            time_limit_result = tk.messagebox.askquestion(title="Time limit reached", message="Continue?")
            human_timer_result = None
            while human_timer_result is None:
                if time_limit_result == 'yes':
                    human_timer_result = time_limit_result
                    self.human_start = time.perf_counter()
                elif time_limit_result == 'no':
                    exit(0)
        print(f"Clicked at {event.x}, {event.y}")

        for row in range(self.hexes_across):
            row_key = self.get_row_key(row)
            selected_row = self.game_board.get(row_key)

            for col in range(Converter.calculate_row_length(row)):
                piece_x_pos = selected_row[col].get("x_pos")
                piece_y_pos = selected_row[col].get("y_pos")

                # ensures clicked area is within the drawn board piece along the x-axis
                if piece_x_pos - RANGE <= event.x <= piece_x_pos + RANGE:

                    # ensures clicked area is within the drawn board piece along the y-axis
                    if piece_y_pos - RANGE <= event.y <= piece_y_pos + RANGE:
                        selected_piece_color = selected_row[col].get("turn_color")

                        piece_clicked = Converter.internal_notation_to_external(row, col)
                        print(f"Selected piece at: {piece_clicked} {self.game_board[row_key][col]['turn_color']}\n")  # prints clicked piece

                        # ensures that the turn turn_color can't select the opposing turn_color's pieces for movement
                        if selected_piece_color == self.turn:

                            if selected_row[col]["selected"]:

                                # gets the index of the selected game piece and calls a helper method
                                index_of_selected_piece = self.selected_pieces_xy_coords.index(
                                    (piece_x_pos, piece_y_pos))
                                self.handle_selecting_selected_piece(index_of_selected_piece)

                            elif self.num_pieces_selected <= 3:

                                # handles logic for the first piece to be selected
                                if self.num_pieces_selected == 0:
                                    # TODO refactor code block below to its own method
                                    self.num_pieces_selected += 1  # increments number of pieces selected to 1
                                    self.adjacent_spaces = self.Move.get_adj_spaces(row, col)  # gets adjacent spaces
                                    self.draw_game_piece_selection(piece_x_pos, piece_y_pos,
                                                                   self.turn)  # draws game piece selection
                                    self.toggle_selected_flag(row_key, col)  # toggles selected flag
                                    self.selected_pieces.append((row_key, col))  # adds selected piece to a list
                                    self.selected_pieces_xy_coords.append(
                                        (piece_x_pos, piece_y_pos))  # adds xy coords to list

                                # handles logic for the second piece to be selected
                                if self.num_pieces_selected == 1:
                                    # checks if the second piece clicked is adjacent to the first
                                    if piece_clicked in self.adjacent_spaces:
                                        # TODO refactor code block below to its own method
                                        self.num_pieces_selected += 1  # increments number of pieces selected to 1
                                        self.adjacent_spaces = self.Move.get_adj_spaces(row,
                                                                                        col)  # gets adjacent spaces
                                        self.draw_game_piece_selection(piece_x_pos, piece_y_pos,
                                                                       self.turn)  # draws game piece selection
                                        self.toggle_selected_flag(row_key, col)  # toggles selected flag
                                        self.selected_pieces.append((row_key, col))  # adds selected piece to a list
                                        self.selected_pieces_xy_coords.append(
                                            (piece_x_pos, piece_y_pos))  # adds xy coords to list

                                # handles logic for the third piece to be selected
                                if self.num_pieces_selected == 2:
                                    # checks if the third piece clicked is adjacent to the second
                                    if piece_clicked in self.adjacent_spaces:

                                        if self.valid_piece_selection(row_key, col):
                                            # TODO refactor code block below to its own method
                                            self.num_pieces_selected += 1  # increments number of pieces selected to 1
                                            self.adjacent_spaces = self.Move.get_adj_spaces(row,
                                                                                            col)  # gets adjacent spaces
                                            self.draw_game_piece_selection(piece_x_pos, piece_y_pos,
                                                                           self.turn)  # draws game piece selection
                                            self.toggle_selected_flag(row_key, col)  # toggles selected flag
                                            self.selected_pieces.append((row_key, col))  # adds selected piece to a list
                                            self.selected_pieces_xy_coords.append(
                                                (piece_x_pos, piece_y_pos))  # adds xy coords to list

                            if DEBUG_PRINT_STATEMENTS:
                                print("--- Debug ---")
                                print(f"Adj spaces: {self.adjacent_spaces}")
                                print(f"Num selected: {self.num_pieces_selected}")
                                print(f"Selected pieces: {self.selected_pieces}")
                                print(f"XY Coords: {self.selected_pieces_xy_coords}")
                                print("-------------\n")

                        elif self.num_pieces_selected > 0:

                            if self.num_pieces_selected == 1:
                                # gets the possible moves for single piece movement
                                self.possible_inline_moves = self.Move.get_possible_single_moves(self.selected_pieces,
                                                                                                 self.num_pieces_selected,
                                                                                                 self.game_board)
                                if DEBUG_PRINT_STATEMENTS:
                                    print(f"Possible inline moves: {self.possible_inline_moves}")

                                # checks if new space clicked is unoccupied, if so then performs single piece move
                                if piece_clicked in self.possible_inline_moves:
                                    self.store_last_move()  # stores the last AI move

                                    # --- Stores the notation for the human move ---#
                                    direction = self.Move.get_dir_of_selected_pieces([(row_key, col), self.selected_pieces[0]])[0]
                                    selected_piece = self.selected_pieces[0]
                                    selected_piece_external_notation = Converter.internal_notation_to_external(selected_piece[0], selected_piece[1])
                                    human_time_taken = time.perf_counter() - self.human_start
                                    self.latest_human_move = ("i", (selected_piece_external_notation, selected_piece_external_notation), direction)

                                    # TODO refactor code block below to its own method
                                    self.move_single_selected_piece(row, col, piece_x_pos, piece_y_pos)
                                    self.num_pieces_selected = 0  # resets num of pieces selected
                                    self.adjacent_spaces = set()  # resets set
                                    self.possible_inline_moves = set()  # resets set
                                    self.selected_pieces = []  # resets list
                                    self.selected_pieces_xy_coords = []  # resets list

                                    update = self.update_timerbox_and_moves_for_color()
                                    update[1].insert(END, self.latest_human_move)
                                    update[0].insert(END, f"{human_time_taken:.5f}")
                                    self.update_time(human_time_taken)
                                    self.update_total_time()
                                    if self.check_win():
                                        break

                                    self.apply_ai()  # gets, and applies, the AI's move

                            # performs 2 or 3 group piece movements
                            elif self.num_pieces_selected > 1:
                                vector_of_dir = self.Move.get_dir_of_selected_pieces(self.selected_pieces)
                                self.possible_inline_moves = self.Move.get_possible_grouped_moves(self.selected_pieces,
                                                                                                  self.num_pieces_selected,
                                                                                                  self.game_board, self.turn,
                                                                                                  vector_of_dir)
                                if DEBUG_PRINT_STATEMENTS:
                                    print(f"Valid INLINE moves: {self.possible_inline_moves}")

                                if piece_clicked in self.possible_inline_moves.keys():

                                    if self.possible_inline_moves[piece_clicked] == "inline":

                                        self.adjacent_spaces = self.Move.get_adj_spaces(self.selected_pieces[0][0],
                                                                                        self.selected_pieces[0][1])

                                        # if the clicked piece is adjacent to the 1st selected game piece
                                        if piece_clicked in self.adjacent_spaces:
                                            self.store_last_move()  # stores the last AI move

                                            # --- Stores the notation for the human move ---#
                                            first_selected_piece = self.selected_pieces[0]
                                            last_selected_piece = self.selected_pieces[-1]
                                            first_piece_external = Converter.internal_notation_to_external(first_selected_piece[0], first_selected_piece[1])
                                            last_piece_external = Converter.internal_notation_to_external(last_selected_piece[0], last_selected_piece[1])

                                            if self.num_pieces_selected == 3:  # checks for 3 piece inline move
                                                second_selected_piece = self.selected_pieces[1]
                                                second_piece_external = Converter.internal_notation_to_external(second_selected_piece[0], second_selected_piece[1])
                                                human_time_taken = time.perf_counter() - self.human_start
                                                self.latest_human_move = ("i", (first_piece_external, second_piece_external, last_piece_external), vector_of_dir[0])
                                            else:
                                                human_time_taken = time.perf_counter() - self.human_start
                                                self.latest_human_move = ("i", (first_piece_external, last_piece_external), vector_of_dir[0])
                                            # ---------------------------------------------- #

                                            # draws the move on the game board
                                            self.move_single_selected_piece(row, col, piece_x_pos, piece_y_pos)

                                        else:
                                            self.store_last_move()  # stores the last AI move

                                            # --- Stores the notation for the human move ---#
                                            first_selected_piece = self.selected_pieces[0]
                                            last_selected_piece = self.selected_pieces[-1]
                                            first_piece_external = Converter.internal_notation_to_external(first_selected_piece[0], first_selected_piece[1])
                                            last_piece_external = Converter.internal_notation_to_external(last_selected_piece[0], last_selected_piece[1])

                                            if self.num_pieces_selected == 3:  # checks for 3 piece inline move
                                                second_selected_piece = self.selected_pieces[1]
                                                second_piece_external = Converter.internal_notation_to_external(second_selected_piece[0], second_selected_piece[1])
                                                human_time_taken = time.perf_counter() - self.human_start
                                                self.latest_human_move = ("i", (first_piece_external, second_piece_external, last_piece_external), vector_of_dir[-1])
                                            else:
                                                human_time_taken = time.perf_counter() - self.human_start
                                                self.latest_human_move = ("i", (first_piece_external, last_piece_external), vector_of_dir[-1])
                                            # ---------------------------------------------- #

                                            # draws the move on the game board
                                            self.move_single_selected_piece(row, col, piece_x_pos, piece_y_pos, index=0)

                                        # TODO refactor code block below to its own method
                                        self.deselect_pieces()  # deselects and toggles "selected" flag on pieces
                                        self.num_pieces_selected = 0  # resets num of pieces selected
                                        self.adjacent_spaces = set()  # resets set
                                        self.possible_inline_moves = set()  # resets set
                                        self.selected_pieces = []  # resets list
                                        self.selected_pieces_xy_coords = []  # resets list

                                        update = self.update_timerbox_and_moves_for_color()
                                        update[1].insert(END, self.latest_human_move)
                                        update[0].insert(END, f"{human_time_taken:.5f}")
                                        self.update_time(human_time_taken)
                                        self.update_total_time()
                                        if self.check_win():
                                            break

                                        self.apply_ai()  # gets, and applies, the AI's move

                                        if DEBUG_PRINT_STATEMENTS:
                                            print("\n--- Debug ---")
                                            print(f"Black turn num: {self.turn_count_black}")
                                            print(f"White turn num: {self.turn_count_white}")
                                            print("-------------\n")

                                    # checks if the player is trying to perform a sumito
                                    elif self.possible_inline_moves[piece_clicked] == "sumito":
                                        valid_sumito = self.is_valid_sumito(row_key, col)

                                        if valid_sumito:
                                            self.store_last_move()  # stores the last AI move

                                            # --- Stores the notation for the human move ---#
                                            first_selected_piece = self.selected_pieces[0]
                                            last_selected_piece = self.selected_pieces[-1]
                                            first_piece_external = Converter.internal_notation_to_external(first_selected_piece[0], first_selected_piece[1])
                                            last_piece_external = Converter.internal_notation_to_external(last_selected_piece[0], last_selected_piece[1])

                                            if self.num_pieces_selected == 3:  # checks for 3 piece inline move
                                                second_selected_piece = self.selected_pieces[1]
                                                second_piece_external = Converter.internal_notation_to_external(second_selected_piece[0], second_selected_piece[1])
                                                human_time_taken = time.perf_counter() - self.human_start
                                                self.latest_human_move = ("i", (first_piece_external, second_piece_external, last_piece_external), vector_of_dir[0])
                                            else:
                                                human_time_taken = time.perf_counter() - self.human_start
                                                self.latest_human_move = ("i", (first_piece_external, last_piece_external), vector_of_dir[0])
                                            # ---------------------------------------------- #

                                            # call method to perform sumito (shift pieces, account for off board push)
                                            self.execute_sumito()

                                            self.deselect_pieces()  # deselects and toggles "selected" flag on pieces
                                            self.num_pieces_selected = 0  # resets num of pieces selected
                                            self.adjacent_spaces = set()  # resets set
                                            self.possible_inline_moves = set()  # resets set
                                            self.selected_pieces = []  # resets list
                                            self.selected_pieces_xy_coords = []  # resets list

                                            update = self.update_timerbox_and_moves_for_color()
                                            update[1].insert(END, self.latest_human_move)
                                            update[0].insert(END, f"{human_time_taken:.5f}")
                                            self.update_time(human_time_taken)
                                            self.update_total_time()
                                            if self.check_win():
                                                break

                                            self.apply_ai()  # gets, and applies, the AI's move

                                        # clears the chain of sumito'ed pieces
                                        self.sumito_chain = []

                                else:
                                    # gets all possible sidestep moves
                                    self.possible_sidestep_moves = self.Move.get_valid_sidestep_moves(self.selected_pieces, self.num_pieces_selected, self.game_board, self.turn, vector_of_dir)

                                    if DEBUG_PRINT_STATEMENTS:
                                        print(f"Valid SIDESTEP moves: {self.possible_sidestep_moves}")

                                    # iterates through all possible side step moves and checks if the 1st piece selected
                                    # is the same as the first piece selected for all possible sidestep moves
                                    for valid_sidestep_pieces in self.possible_sidestep_moves:

                                        piece_clicked_internal_notation = Converter.external_notation_to_internal(piece_clicked)
                                        if piece_clicked_internal_notation == valid_sidestep_pieces[0][0] and self.num_pieces_selected == len(valid_sidestep_pieces[0]):
                                            self.store_last_move()  # stores the last AI move

                                            # --- Stores the notation for the human move ---#
                                            direction = valid_sidestep_pieces[1]
                                            first_selected_piece = self.selected_pieces[0]
                                            last_selected_piece = self.selected_pieces[-1]
                                            first_piece_external = Converter.internal_notation_to_external(first_selected_piece[0], first_selected_piece[1])
                                            last_piece_external = Converter.internal_notation_to_external(last_selected_piece[0], last_selected_piece[1])

                                            if self.num_pieces_selected == 3:  # checks for 3 piece inline move
                                                second_selected_piece = self.selected_pieces[1]
                                                second_piece_external = Converter.internal_notation_to_external(second_selected_piece[0], second_selected_piece[1])
                                                human_time_taken = time.perf_counter() - self.human_start
                                                self.latest_human_move = ("s", (first_piece_external, second_piece_external, last_piece_external), direction)
                                            else:
                                                human_time_taken = time.perf_counter() - self.human_start
                                                self.latest_human_move = ("s", (first_piece_external, last_piece_external), direction)
                                            # ---------------------------------------------- #

                                            # helper method to perform the sidestep move
                                            self.perform_sidestep(valid_sidestep_pieces)
                                            update = self.update_timerbox_and_moves_for_color()
                                            update[1].insert(END, self.latest_human_move)
                                            update[0].insert(END, f"{human_time_taken:.5f}")
                                            self.update_time(human_time_taken)
                                            self.update_total_time()
                                            if self.check_win():
                                                break

                                            self.apply_ai()  # gets, and applies, the AI's move

    def undo_last_move(self):
        """
        Performs an undo from before the latest move was made.
        """
        if len(self.previous_board_states) > 0:
            previous_state = self.previous_board_states.pop()

            # deletes content within the black & white, timer & moves box
            self.repopulate_listbox(self.black_timer_box, previous_state["black_timer_box"])
            self.repopulate_listbox(self.white_timer_box, previous_state["white_timer_box"])

            self.repopulate_listbox(self.black_moves_box, previous_state["black_moves"])
            self.repopulate_listbox(self.white_moves_box, previous_state["white_moves"])

            # undoes the black and white move count
            self.black_move_count = previous_state["black_move_count"]
            self.white_move_count = previous_state["white_move_count"]

            # undoes the black and white piece count
            self.black_pieces = previous_state["black_pieces"]
            self.white_pieces = previous_state["white_pieces"]

            # undoes the state of the game board
            self.game_board = previous_state["game_board"]

            # resets ALL movement related data attributes
            self.adjacent_spaces = set()
            self.possible_inline_moves = set()
            self.possible_sidestep_moves = []
            self.selected_pieces = []
            self.selected_pieces_xy_coords = []
            self.num_pieces_selected = 0
            self.sumito_chain = []  # resets the chain of pieces to be sumito, in order
            self.dir_tuple_sumito = ()  # resets the vector of direction for the sumito chain
            self.first_piece_selection = None  # resets the index of piece adjacent to first piece in sumito chain
            self.latest_human_move = ()  # resets the latest human move

            self.remove_selection_flag()

            # redraws the game board and updates the black and white move and piece count
            self.draw_game_board()
            self.initialize_game_board_pieces()
            self.player_info()

    def remove_selection_flag(self):
        """
        Removes the "selected" piece flag for all game pieces
        """
        for row in self.game_board:
            for col in self.game_board[row]:
                if col["selected"]:
                    col["selected"] = False

    def repopulate_listbox(self, listbox, content):
        """
        Repopulates the Listbox with it's updated content
        """
        if len(content) > 0:
            listbox.delete(2, END)

            for item in content:
                listbox.insert(END, item)
        else:
            listbox.delete(2, END)

    def store_last_move(self):
        """
        Stores the entire game state to allow the undo button to function
        """
        game_board = deepcopy(self.game_board)

        black_move_count = self.black_move_count
        white_move_count = self.white_move_count

        black_pieces = self.black_pieces
        white_pieces = self.white_pieces

        black_timer_box = self.black_timer_box.get(2, END)
        white_timer_box = self.white_timer_box.get(2, END)

        black_moves = self.black_moves_box.get(2, END)
        white_moves = self.white_moves_box.get(2, END)

        current_game_state = {"game_board": game_board,
                              "black_move_count": black_move_count, "white_move_count": white_move_count,
                              "black_pieces": black_pieces, "white_pieces": white_pieces,
                              "black_timer_box": black_timer_box, "white_timer_box": white_timer_box,
                              "black_moves": black_moves, "white_moves": white_moves}

        if len(self.previous_board_states) == 10:
            self.previous_board_states.pop(0)

        self.previous_board_states.append(current_game_state)

    def apply_ai(self):
        """
        Gets the AI's move, and then redraws the game board with the AI's new move.
        """
        if not self.human_vs_human:
            self.store_last_move()  # stores the last AI move

            self.increment_turn_count()  # increments turn count of current turn turn_color
            # self.update_timer()

            start = time.perf_counter()

            self.turn = Converter.get_opposite_color(self.turn)  # turn turn_color change
            if self.turn == "black":
                turn_timer = self.settings_selections['time1']
            else:
                turn_timer = self.settings_selections['time2']

            result = self.Minimax.alpha_beta(["move", self.game_board, self.turn, 0, start, turn_timer])  # gets move and board from ai choice
            self.game_board = result[1]  # ai selected board
            selected_move = result[0]  # the move needs to print to the game console and show highlighted ai pieces
            time_taken = time.perf_counter() - start

            print("Ai selected move" + str(selected_move))

            # redraws new game board generated from AI within ai.py from line above
            self.draw_game_board()
            update = self.update_timerbox_and_moves_for_color()
            update[0].insert(END, f"{time_taken:.5f}")
            update[1].insert(END, selected_move[:3])
            self.update_time(time_taken)
            self.update_total_time()

            self.initialize_game_board_pieces()
            self.increment_turn_count()  # increments turn count of current turn turn_color
            self.player_info()

            self.highlight_ai_move(selected_move)  # highlights the AI move yellow

            self.turn = Converter.get_opposite_color(self.turn)  # turn turn_color change
            self.human_start = time.perf_counter()

            self.update_piece_count()
        else:  # handles Human vs Human
            self.store_last_move()  # stores the last AI move
            self.increment_turn_count()  # increments turn count of current turn turn_color
            self.turn = Converter.get_opposite_color(self.turn)  # turn turn_color change
            self.player_info()
        self.human_start = time.perf_counter()

    def update_piece_count(self):
        """
        Updates the piece count (or pieces lost) for the human player when playing against the AI.
        """
        piece_count = 0
        for row in self.game_board:
            entire_row = self.game_board[row]
            for column in entire_row:
                if column["turn_color"] == self.turn:
                    piece_count += 1

        if self.turn == "black":
            self.black_pieces = piece_count
        else:
            self.white_pieces = piece_count
        self.player_info()

    def highlight_ai_move(self, selected_move: list):
        """
        Handles highlighting the AI's most recent move.
        :param selected_move: a list, containing the type of move and pieces moved
        """
        piece_to_move = Converter.external_notation_to_internal(selected_move[1][-1])
        cardinal_dir = selected_move[2]

        # sets the number of iterations to check and highlight AI moved pieces depending if the move was
        # a sidestep or inline
        if selected_move[0] == "s":
            iterations = range(0, len(selected_move[1]))  # subtract 1 as 1 piece is already moved on line before 'try'
        elif selected_move[1][0] == selected_move[1][-1]:  # checks for single piece move
            iterations = range(0, 1)
        else:
            iterations = range(0, 3)

        for iteration in iterations:

            try:
                dir_tuple = self.Move.get_adjusted_tuple_or_cardinal_dir(piece_to_move[0], cardinal_dir=cardinal_dir)
                piece_to_move = Converter.simulate_game_piece_movement(piece_to_move[0], piece_to_move[1], dir_tuple)

                if piece_to_move[1] > 0:
                    # handles highlighting pieces for inline moves
                    if selected_move[0] == "i":
                        if self.game_board[piece_to_move[0]][piece_to_move[1]]["turn_color"] == self.turn:
                            # extracts x and y coords and highlights moved pieces
                            piece_x_pos = self.game_board[piece_to_move[0]][piece_to_move[1]]["x_pos"]
                            piece_y_pos = self.game_board[piece_to_move[0]][piece_to_move[1]]["y_pos"]
                            self.draw_game_piece_selection(piece_x_pos, piece_y_pos, self.turn, "red")
                    elif selected_move[0] == "s":
                        if self.game_board[piece_to_move[0]][piece_to_move[1]]["turn_color"] == self.turn:
                            # extracts x and y coords and highlights moved pieces
                            piece_x_pos = self.game_board[piece_to_move[0]][piece_to_move[1]]["x_pos"]
                            piece_y_pos = self.game_board[piece_to_move[0]][piece_to_move[1]]["y_pos"]
                            self.draw_game_piece_selection(piece_x_pos, piece_y_pos, self.turn, "red")

                            # sets the next piece to the next piece within selected_move[1]
                            piece_to_move = Converter.external_notation_to_internal(selected_move[1][iteration])
            except (IndexError, KeyError):
                pass

    def update_timerbox_and_moves_for_color(self):
        if self.turn == "black":
            return [self.black_timer_box, self.black_moves_box]
        else:
            return [self.white_timer_box, self.white_moves_box]

    def update_time(self, time):
        if self.turn == "black":
            self.black_total_time += time
        else:
            self.white_total_time += time

    def perform_sidestep(self, sidestep_move_details: list):
        """
        Performs the sidestep. Involves drawing the new pieces to the new location, removing where the old pieces were
        on the game board, and within game_board updating the "selected" and "turn_color" flags.
        :param sidestep_move_details: a list, containing a list of new spaces and the direction of movement
        """
        for _ in range(0, self.num_pieces_selected):
            new_spaces = sidestep_move_details[0]  # new_spaces is a list of internal game board coords
            new_space = new_spaces.pop()
            new_row = new_space[0]  # gets row of new space
            new_col = new_space[1]  # gets col of new space
            new_x_pos = self.game_board[new_space[0]][new_space[1]]["x_pos"]  # gets x coordinates of new position
            new_y_pos = self.game_board[new_space[0]][new_space[1]]["y_pos"]  # gets y coordinates of new position

            self.move_single_selected_piece(new_row, new_col, new_x_pos, new_y_pos)  # draws new piece

        self.possible_sidestep_moves = []  # clears the list of valid sidestep moves

    def is_valid_sumito(self, piece_clicked_row: str, piece_clicked_col: int) -> bool:
        """
        Determines if the proposed sumito is valid ir not, and returns True if it is.
        :return: a boolean
        """
        # adds the first piece for the sumito check to the sumito piece list
        self.sumito_chain.append((piece_clicked_row, piece_clicked_col))

        # gets internal notation for piece to check sumito for, and gets adjacent spaces
        sumito_piece_adj_spaces = self.Move.get_adj_spaces(piece_clicked_row, piece_clicked_col)

        # finds the piece of the turn turn_color closest to piece to check sumito for
        adjacent_piece_internal = None
        for adjacent_selected_piece in self.selected_pieces:
            # gets internal notation of selected pieces for following membership check
            adjacent_selected_piece_external = Converter.internal_notation_to_external(adjacent_selected_piece[0],
                                                                                       adjacent_selected_piece[1])
            if adjacent_selected_piece_external in sumito_piece_adj_spaces:
                adjacent_piece_internal = Converter.external_notation_to_internal(adjacent_selected_piece_external)

                # gets the last piece in the selected piece chain that ISN'T adjacent to the 1st piece in sumito chain
                if self.selected_pieces.index(adjacent_selected_piece) == 0:
                    self.first_piece_selection = -1
                else:
                    self.first_piece_selection = 0

        # gets vector of direction for selected piece and sumito piece to find num of
        # adjacent opposing turn_color pieces
        vector_of_dir_for_sumito_check = self.Move.get_dir_of_selected_pieces(
            [adjacent_piece_internal, (piece_clicked_row, piece_clicked_col)])

        # iterates through the list of directions, finds the correct vector to get num of adj opposing turn_color pieces,
        # and returns this number
        for direction in vector_of_dir_for_sumito_check:
            dir_tuple = self.Move.get_adjusted_tuple_or_cardinal_dir(piece_clicked_row, cardinal_dir=direction)

            # resets the piece to be checked
            adj_piece = (piece_clicked_row, piece_clicked_col)

            # checks if there are 2 pieces adjacent to the piece to be sumito'ed
            for num in range(0, 2):
                adj_piece = Converter.simulate_game_piece_movement(adj_piece[0], adj_piece[1], dir_tuple)

                # catches game space checks that might be out of bounds
                try:
                    # ensures the column isn't out of bounds
                    if adj_piece[1] < 0:
                        raise KeyError

                    # checks if the next adjacent piece is the opposing turn_color
                    elif self.game_board[adj_piece[0]][adj_piece[1]]["turn_color"] == Converter.get_opposite_color(self.turn):
                        self.sumito_chain.append((adj_piece[0], adj_piece[1]))

                    # gets the vector of direction of sumito chain by reversing direction of selected pieces chain
                    elif self.game_board[adj_piece[0]][adj_piece[1]]["turn_color"] == self.turn:
                        direction_cardinal_index = vector_of_dir_for_sumito_check.index(direction)

                        # gets the opposite cardinal direction
                        if direction_cardinal_index == 0:
                            sumito_dir_cardinal = vector_of_dir_for_sumito_check[1]
                        else:
                            sumito_dir_cardinal = vector_of_dir_for_sumito_check[0]
                        self.dir_tuple_sumito = self.Move.get_adjusted_tuple_or_cardinal_dir(piece_clicked_row, cardinal_dir=sumito_dir_cardinal)

                    # stops searching for 3rd adjacent sumito chain piece if there isn't a 2nd
                    else:
                        break

                except (IndexError, KeyError):
                    pass

        if len(self.sumito_chain) < self.num_pieces_selected:
            return True
        else:
            return False

    def execute_sumito(self):
        """
        Executes the sumito. This involves updating the game_board dictionary, and drawing the correct game board state.
        """
        last_piece_in_chain = self.sumito_chain[-1]
        space_behind_sumito_chain = Converter.simulate_game_piece_movement(last_piece_in_chain[0],
                                                                           last_piece_in_chain[1],
                                                                           self.dir_tuple_sumito)
        opposite_color = Converter.get_opposite_color(self.turn)

        try:
            # if column is out of bounds then that means piece is pushed off board
            if space_behind_sumito_chain[1] < 0:
                raise KeyError

            # pushes the sumito chain
            elif self.game_board[space_behind_sumito_chain[0]][space_behind_sumito_chain[1]]["turn_color"] == None:
                # logic for updating game board and drawing

                # gets first piece in sumito chain and places it behind the sumito chain
                self.game_board[space_behind_sumito_chain[0]][space_behind_sumito_chain[1]][
                    "turn_color"] = opposite_color
                behind_space_x_pos = self.game_board[space_behind_sumito_chain[0]][space_behind_sumito_chain[1]][
                    "x_pos"]
                behind_space_y_pos = self.game_board[space_behind_sumito_chain[0]][space_behind_sumito_chain[1]][
                    "y_pos"]
                self.draw_game_piece(behind_space_x_pos, behind_space_y_pos, opposite_color)

        # means that the piece is pushed off the board
        except (IndexError, KeyError):
            # decrements the piece count for the opposing turn_color
            if self.turn == "black":
                self.white_pieces -= 1
            else:
                self.black_pieces -= 1

            pushed_off_piece = self.sumito_chain[-1]
            pushed_off_piece_internal = Converter.internal_notation_to_external(pushed_off_piece[0],
                                                                                pushed_off_piece[1])
            print(f"{pushed_off_piece_internal}{opposite_color[0].lower()} pushed off the board!")

            # debug
            print(f"Num of Black: {self.black_pieces}")
            print(f"Num of White: {self.white_pieces}")

        finally:
            # gets the first piece in the sumito chain and changes it to the turn turn_color
            first_sumito_piece = self.sumito_chain[0]
            first_sumito_piece_x_pos = self.game_board[first_sumito_piece[0]][first_sumito_piece[1]]["x_pos"]
            first_sumito_piece_y_pos = self.game_board[first_sumito_piece[0]][first_sumito_piece[1]]["y_pos"]
            self.move_single_selected_piece(first_sumito_piece[0], first_sumito_piece[1], first_sumito_piece_x_pos,
                                            first_sumito_piece_y_pos, self.first_piece_selection)

    def valid_piece_selection(self, row_key, col):
        """
        Checks if third piece selected is valid
        :return: a boolean
        """
        inline_row = 0
        inline_col = 0
        if self.selected_pieces[0][0] == self.selected_pieces[1][0]:
            inline_row += 1
        if self.selected_pieces[0][1] == self.selected_pieces[1][1]:
            inline_col += 1
        for piece in self.selected_pieces:
            if piece[0] == row_key:
                inline_row += 1
            if piece[1] == col:
                inline_col += 1
        # checks if the selected pieces are inline
        if inline_row != len(self.selected_pieces) - 1:
            if self.selected_pieces[0][1] != self.selected_pieces[1][1]:
                if self.selected_pieces[0][1] == col:
                    return False

            if (row_key != "row3" or self.selected_pieces[0][0] != "row5") and (row_key != "row5" or self.selected_pieces[0][0] != "row3"):
                if inline_col != len(self.selected_pieces) - 1:
                    return True
                else:
                    return False
            elif row_key == "row3" and inline_col != 3:
                return True
            elif row_key == "row5" and inline_col != 3:
                return True
            else:
                return False

    def increment_turn_count(self):
        """
        Increments the turn count for the current turn's turn_color.
        """
        if self.turn == "black":
            self.turn_count_black += 1
            self.black_move_count -= 1
        else:
            self.turn_count_white += 1
            self.white_move_count -= 1

    def move_single_selected_piece(self, new_row_num: int, new_col_num: int, new_x_pos: int, new_y_pos: int, index=-1):
        """
        Moves the game piece. The method draws the new game pieces, removes the old game piece, toggles the "selected"
        flag, and then updates the game board "turn_color" value for both the new space and old space.
        :param new_row_num: an int, the new row number to move to
        :param new_col_num: an int, the new column number to move to
        :param new_x_pos: an int, the x coordinates of the new space
        :param new_y_pos: an int, the y coordinates of the new space
        :param index: an int, the index of the piece to be moved
        """

        if type(new_row_num) != int:
            new_row_num = Converter.convert_row_to_string_or_int(new_row_num)

        selected_piece_internal_coords = self.selected_pieces.pop(index)
        selected_piece_xy_coords = self.selected_pieces_xy_coords.pop(index)
        self.num_pieces_selected -= 1

        self.draw_game_piece(selected_piece_xy_coords[0], selected_piece_xy_coords[1], "slate grey")
        self.draw_game_piece(new_x_pos, new_y_pos, self.turn)

        self.toggle_selected_flag(selected_piece_internal_coords[0], selected_piece_internal_coords[1])

        self.game_board[selected_piece_internal_coords[0]][selected_piece_internal_coords[1]]["turn_color"] = None
        self.game_board[Converter.convert_row_to_string_or_int(new_row_num)][new_col_num]["turn_color"] = self.turn

    def handle_selecting_selected_piece(self, index_of_selected_piece: int):
        """
        Handles the logic for when an already-selected game piece is selected again. The following occurs when an
        already selected game piece is clicked on again:

            - If 1, 2, or 3 game pieces are currently selected and the 1st selected game piece is clicked, all selected
              pieces are deselected
            - If 2 or 3 game pieces are selected and the 2nd selected game piece is elected then all pieces but the 1st
              selected game piece is deselected

        :param index_of_selected_piece: an int, of the selected game piece
        """

        # handles logic when 1st selected piece is selected again
        if index_of_selected_piece == 0:
            self.deselect_pieces()  # 0 means all currently selected pieces are deselected
            self.adjacent_spaces = set()  # empties the adjacent spaces set

        # handles logic when 2nd selected piece is selected again
        elif index_of_selected_piece == 1:
            self.deselect_pieces(1)  # 1 here deselects all pieces but the 1st selected piece

            # gets the internal coordinates of the selected piece and gets the adjacent spaces to it
            first_piece_internal = self.selected_pieces[0]  # gets the 1st selected piece
            self.adjacent_spaces = self.Move.get_adj_spaces(first_piece_internal[0], first_piece_internal[1])

        # handles logic when 3rd selected piece is selected again
        elif index_of_selected_piece == 2:

            # gets the internal coordinates of the 2nd selected piece and gets the adjacent spaces to it
            second_piece_internal_coords = self.selected_pieces[
                1]  # 2nd selected piece is always index 1 within self.selected_pieces
            self.adjacent_spaces = self.Move.get_adj_spaces(second_piece_internal_coords[0],
                                                            second_piece_internal_coords[1])

            # removes coords of 3rd piece from the list and toggles its 'selected' flag
            deselected_piece_internal_coords = self.selected_pieces.pop()  # removes the 3rd, selected piece from the list
            self.toggle_selected_flag(deselected_piece_internal_coords[0],
                                      deselected_piece_internal_coords[1])  # toggles selected flag

            # gets the x and y coords of the 3rd selected piece and "unselects" it
            deselected_piece_xy_coords = self.selected_pieces_xy_coords.pop()
            self.draw_game_piece(deselected_piece_xy_coords[0], deselected_piece_xy_coords[1], self.turn)

            # decrements number of pieces selected
            self.num_pieces_selected -= 1

    def deselect_pieces(self, lower_bound=0, piece_color=None):
        """
        Unselects all the selected game pieces within the provided range. The lower bound is specified when the second
        selected piece is clicked again to deselect all pieces but the first selected piece.
        :param lower_bound: an int, either 0 by default or 1.
        """
        ZERO_INDEX_OFFSET = 1

        # iterates over the number of selected pieces and de-selects them if the second selected piece is clicked again
        for iteration in range(lower_bound, self.num_pieces_selected):
            # removes coords from piece in the last position of list and toggles its flag
            deselected_piece_internal_coords = self.selected_pieces.pop()  # removes the last, selected piece from the list
            self.toggle_selected_flag(deselected_piece_internal_coords[0],
                                      deselected_piece_internal_coords[1])  # toggles selected flag

            # gets the x and y coords of the last piece in the list and "unselects" it, and draws over it entirely
            deselected_piece_xy_coords = self.selected_pieces_xy_coords.pop()
            if piece_color == None:
                piece_color = self.turn
            self.draw_game_piece(deselected_piece_xy_coords[0], deselected_piece_xy_coords[1], piece_color)

            # decrements number of pieces selected
            self.num_pieces_selected -= 1

    def toggle_selected_flag(self, row_key, col_num: int):
        """
        Toggles the "selected" flag for the provided game piece.
        :param row_key: a string, or an int, of the row of the selected piece
        :param col_num: an int, of the column of the selected piece
        """

        # if the row passed is an int, it is converted to a string so it can be used as a key within the game board dict
        if type(row_key) != str:
            row_key = Converter.convert_row_to_string_or_int(row_key)

        selected_piece = self.game_board.get(row_key)[col_num]
        if not selected_piece["selected"]:
            selected_piece["selected"] = True
        else:
            selected_piece["selected"] = False

    def draw_game_piece(self, piece_x_pos: float, piece_y_pos: float, piece_color: str):
        """
        Draws the specified turn_color game piece at the specified x and y coordinates.
        :param piece_x_pos: a float
        :param piece_y_pos: a float
        :param piece_color: a string, either 'white' or 'black'
        """
        self.canvas.create_oval(piece_x_pos - self.piece_radius,
                                piece_y_pos - self.piece_radius,
                                piece_x_pos + self.piece_radius,
                                piece_y_pos + self.piece_radius, fill=piece_color)

    def draw_game_piece_selection(self, piece_x_pos: float, piece_y_pos: float, piece_color: str, selection_color="green"):
        """
        Draws the green circle on the game piece that the player has clicked on to select for movement.
        :param piece_x_pos: a float
        :param piece_y_pos: a float
        :param piece_color: a string, either 'white' or 'black'
        """
        self.canvas.create_oval(piece_x_pos - self.selection_radius,
                                piece_y_pos - self.selection_radius,
                                piece_x_pos + self.selection_radius,
                                piece_y_pos + self.selection_radius, fill=selection_color)

        self.canvas.create_oval(piece_x_pos - self.selection_redraw_radius,
                                piece_y_pos - self.selection_redraw_radius,
                                piece_x_pos + self.selection_redraw_radius,
                                piece_y_pos + self.selection_redraw_radius,
                                fill=piece_color)

    def draw_game_board(self):
        """
        Draws the hexagonal shape of the board.
        """
        x_pos = self.width // 2
        y_pos = self.height // 2
        radius = 500 // 2
        cos60 = math.cos(math.pi / 3)
        sin60 = math.sin(math.pi / 3)
        self.canvas.create_polygon(x_pos - radius, y_pos, x_pos - radius * cos60, y_pos - radius * sin60, x_pos +
                                   radius * cos60, y_pos - radius * sin60, x_pos + radius, y_pos, x_pos + radius *
                                   cos60, y_pos + radius * sin60, x_pos - radius * cos60, y_pos + radius * sin60,
                                   fill=self.bg)
        self.draw_board_spaces(x_pos, y_pos, radius, sin60)
        self.canvas.grid(row=2, column=2, rowspan=25, columnspan=3)

    def draw_board_spaces(self, x_pos: int, y_pos: int, radius: int, sin60: float):
        """
        Iterates through the game board containing the representation of the game board and draws a circle to represent
        a game board space in the appropriate location.
        :param x_pos: an int
        :param y_pos: an int
        :param radius: an int
        :param sin60: a float
        """
        for row in range(self.hexes_across):
            row_key = self.get_row_key(row)
            spot_y = (y_pos - radius * sin60) + (row * self.hex_size * sin60) + (self.hex_size * sin60 / 2)
            row_length = Converter.calculate_row_length(row)
            start_x = x_pos - (row_length * self.hex_size // 2) + (self.hex_size // 2)
            for col in range(row_length):
                spot_x = start_x + col * self.hex_size
                self.canvas.create_oval(spot_x - self.spot_radius, spot_y - self.spot_radius,
                                        spot_x + self.spot_radius, spot_y + self.spot_radius, fill="slate grey")

                # populates game_board dictionary with coordinates of each game piece based on the specified game layout
                if not self.game_board.get(row_key)[col]["x_pos"]:
                    self.game_board.get(row_key)[col].update({"x_pos": int(spot_x)})
                    self.game_board.get(row_key)[col].update({"y_pos": int(spot_y)})

    def initialize_game_board_pieces(self):
        """
        Iterates through the game_board data structure, retrieves the x and y coordinates of each board space,
        and draws the game piece on the board of appropriate specified turn_color.
        """
        for row in range(self.hexes_across):
            row_key = self.get_row_key(row)
            row_length = Converter.calculate_row_length(row)

            for col in range(row_length):
                piece_color = self.game_board.get(row_key)[col].get("turn_color")
                piece_x = self.game_board.get(row_key)[col].get("x_pos")  # x coordinates of the selected piece
                piece_y = self.game_board.get(row_key)[col].get("y_pos")  # y coordinates of the selected piece

                self.draw_game_piece(piece_x, piece_y, piece_color)

    def initialize_default_layout(self):
        """
        Initializes the game board array representing the game board with the game pieces of each turn_color in the standard,
        default, layout.
        """
        lines_to_fill = 2

        for row in range(lines_to_fill):
            row_key = "row" + str(row)

            for col in range(Converter.calculate_row_length(row)):
                self.game_board.get(row_key)[col].update({"turn_color": "white"})

                if row == 1:  # populates front 3 white pieces
                    for nested_col in range(2, 5):
                        self.game_board.get("row2")[nested_col].update({"turn_color": "white"})

        for row in range(7, 9):
            row_key = "row" + str(row)

            if (row - 1) == 6:  # populates front 3 black pieces
                for nested_col in range(2, 5):
                    self.game_board.get("row6")[nested_col].update({"turn_color": "black"})
            for col in range(Converter.calculate_row_length(row)):
                self.game_board.get(row_key)[col].update({"turn_color": "black"})

    def initialize_german_layout(self):
        """
        Initializes the game board array representing the game board with the game pieces of each turn_color in the German
        daisy layout.
        """
        ZERO_INDEX_OFFSET = 1
        lines_to_fill = 2 + ZERO_INDEX_OFFSET

        # populates top half of the game board (rows I to F)
        for row in range(lines_to_fill):
            row_key = "row" + str(row)

            for col in range(Converter.calculate_row_length(row)):

                if row == 0:  # populates game pieces on the first row (row I)
                    if col in range(0, 1 + ZERO_INDEX_OFFSET):  # populates 2 white pieces on first row (row I)
                        self.game_board[row_key][col].update({"turn_color": "white"})

                    if col in range(3, 4 + ZERO_INDEX_OFFSET):  # populates 2 black pieces on first row (row I)
                        self.game_board[row_key][col].update({"turn_color": "black"})

                if row == 1:  # populates game pieces on the second row (row H)
                    if col in range(0, 2 + ZERO_INDEX_OFFSET):  # populates 3 white pieces on second row (row H)
                        self.game_board[row_key][col].update({"turn_color": "white"})

                    if col in range(3, 5 + ZERO_INDEX_OFFSET):  # populates 3 black pieces on second row (row H)
                        self.game_board[row_key][col].update({"turn_color": "black"})

                if row == 2:  # populates game pieces on the third row (row G)
                    if col in range(1, 2 + ZERO_INDEX_OFFSET):  # populates 2 white pieces on third row (row G)
                        self.game_board[row_key][col].update({"turn_color": "white"})

                    if col in range(4, 5 + ZERO_INDEX_OFFSET):  # populates 2 black pieces on third row (row G)
                        self.game_board[row_key][col].update({"turn_color": "black"})

        # populates lower half of the game board (rows C to D)
        for row in range(6, 8 + ZERO_INDEX_OFFSET):
            row_key = "row" + str(row)

            for col in range(Converter.calculate_row_length(row)):

                if row == 6:  # populates game pieces on the seventh row (row C)
                    if col in range(1, 2 + ZERO_INDEX_OFFSET):  # populates 2 black pieces on seventh row (row C)
                        self.game_board[row_key][col].update({"turn_color": "black"})

                    if col in range(4, 5 + ZERO_INDEX_OFFSET):  # populates 2 white pieces on seventh row (row C)
                        self.game_board[row_key][col].update({"turn_color": "white"})

                if row == 7:  # populates game pieces on the eighth row (row B)
                    if col in range(0, 2 + ZERO_INDEX_OFFSET):  # populates 3 black pieces on eighth row (row B)
                        self.game_board[row_key][col].update({"turn_color": "black"})

                    if col in range(3, 5 + ZERO_INDEX_OFFSET):  # populates 3 white pieces on eighth row (row B)
                        self.game_board[row_key][col].update({"turn_color": "white"})

                if row == 8:  # populates game pieces on the ninth row (row A)
                    if col in range(0, 1 + ZERO_INDEX_OFFSET):  # populates 2 black pieces on ninth row (row A)
                        self.game_board[row_key][col].update({"turn_color": "black"})

                    if col in range(3, 4 + ZERO_INDEX_OFFSET):  # populates 2 white pieces on ninth row (row A)
                        self.game_board[row_key][col].update({"turn_color": "white"})

    def initialize_belgian_layout(self):
        """
        Initializes the game board array representing the game board with the game pieces of each turn_color in the Belgian
        daisy layout.
        """
        ZERO_INDEX_OFFSET = 1
        lines_to_fill = 3 + ZERO_INDEX_OFFSET

        # populates top half of the game board (rows I to F)
        for row in range(1, lines_to_fill):
            row_key = "row" + str(row)

            for col in range(Converter.calculate_row_length(row)):

                if row == 1:  # populates game pieces on the second row (row H)
                    if col in range(0, 1 + ZERO_INDEX_OFFSET):  # populates 2 white pieces on second row (row H)
                        self.game_board[row_key][col].update({"turn_color": "white"})

                    if col in range(4, 5 + ZERO_INDEX_OFFSET):  # populates 2 black pieces on second row (row H)
                        self.game_board[row_key][col].update({"turn_color": "black"})

                if row == 2:  # populates game pieces on the third row (row G)
                    if col in range(0, 2 + ZERO_INDEX_OFFSET):  # populates 3 white pieces on second row (row HG)
                        self.game_board[row_key][col].update({"turn_color": "white"})

                    if col in range(4, 6 + ZERO_INDEX_OFFSET):  # populates 3 black pieces on second row (row G)
                        self.game_board[row_key][col].update({"turn_color": "black"})

                if row == 3:  # populates game pieces on the fourth row (row F)
                    if col in range(1, 2 + ZERO_INDEX_OFFSET):  # populates 2 white pieces on second row (row F)
                        self.game_board[row_key][col].update({"turn_color": "white"})

                    if col in range(5, 6 + ZERO_INDEX_OFFSET):  # populates 2 black pieces on second row (row F)
                        self.game_board[row_key][col].update({"turn_color": "black"})

        # populates lower half of the game board (rows C to D)
        for row in range(5, 7 + ZERO_INDEX_OFFSET):
            row_key = "row" + str(row)

            for col in range(Converter.calculate_row_length(row)):

                if row == 5:  # populates game pieces on the sixth row (row D)
                    if col in range(1, 2 + ZERO_INDEX_OFFSET):  # populates 2 black pieces on second row (row D)
                        self.game_board[row_key][col].update({"turn_color": "black"})

                    if col in range(5, 6 + ZERO_INDEX_OFFSET):  # populates 2 white pieces on second row (row D)
                        self.game_board[row_key][col].update({"turn_color": "white"})

                if row == 6:  # populates game pieces on the seventh row (row C)
                    if col in range(0, 2 + ZERO_INDEX_OFFSET):  # populates 3 black pieces on second row (row C)
                        self.game_board[row_key][col].update({"turn_color": "black"})

                    if col in range(4, 6 + ZERO_INDEX_OFFSET):  # populates 3 white pieces on second row (row C)
                        self.game_board[row_key][col].update({"turn_color": "white"})

                if row == 7:  # populates game pieces on the eighth row (row B)
                    if col in range(0, 1 + ZERO_INDEX_OFFSET):  # populates 2 black pieces on second row (row B)
                        self.game_board[row_key][col].update({"turn_color": "black"})

                    if col in range(4, 5 + ZERO_INDEX_OFFSET):  # populates 2 white pieces on second row (row B)
                        self.game_board[row_key][col].update({"turn_color": "white"})

    def initialize_game_board_array(self):
        """
        Initializes the dictionary representing the game board containing arrays of dictionaries that contain the
        various attributes of the game pieces. These attributes are: the column number, piece turn_color, if the piece
        has been clicked on by the player, and the piece's x and y coordinates.
        """
        self.game_board = {}

        for col in range(self.hexes_across):
            row_length = Converter.calculate_row_length(col)
            row_key = "row" + str(col)
            self.game_board.update({row_key: []})

            for row in range(row_length):
                self.game_board.get(row_key).append(
                    {"colNum": row, "turn_color": None, "selected": False, "x_pos": None, "y_pos": None})

    def apply_draw_game_board_layout(self):
        self.initialize_game_board_array()

        game_layout = self.settings_selections["config"]
        if game_layout == 3:
            self.initialize_german_layout()
        elif game_layout == 2:
            self.initialize_belgian_layout()
        else:
            self.initialize_default_layout()

        self.draw_game_board()
        self.initialize_game_board_pieces()

    def make_random_first_move(self) -> list:
        """
        Gets the first random move for black.
        :return: a list, containing the AI's selected move.
        """
        ZERO_INDEX_OFFSET = 1

        start = time.perf_counter()
        StateSpaceGenRandFirstMove = StateSpaceGenerator(self.game_board, self.turn)
        states = StateSpaceGenRandFirstMove.run_generation()

        random_int = random.randint(0, len(states) - ZERO_INDEX_OFFSET)  # gets a random int
        random_state = states[random_int]  # gets a random state with the random int
        time_taken = time.perf_counter() - start

        self.game_board = random_state[1]
        self.draw_game_board()

        update = self.update_timerbox_and_moves_for_color()
        update[0].insert(END, f"{time_taken:.5f}")
        update[1].insert(END, random_state[0][:3])
        self.update_time(time_taken)
        self.update_total_time()

        self.player_info()

        self.initialize_game_board_pieces()
        self.increment_turn_count()  # increments turn count of current turn turn_color

        return random_state[0]

    def ai_vs_ai(self):
        while True:
            if self.check_win():
                break
            self.apply_ai()
            self.turn = Converter.get_opposite_color(self.turn)
            self.update()  # forces tkinter to re-draw the new board despite being blocked by the while-loop

    def check_win(self):

        if self.black_pieces < 8:
            print("White wins! Six Black pieces pushed off the board!")
            return True
        elif self.white_pieces < 8:
            print("Black wins! Six White pieces pushed off the board!")
            return True

            # if turn limit is reached, turn_color with the most marbles pushed off wins, else there is a tie
        elif self.black_move_count == 0 or self.white_move_count == 0:
            if self.black_move_count == 1 or self.white_move_count == 1:
                return False
            elif self.white_pieces < self.black_pieces:
                print("Turn limit reached, Black wins! More White pieces pushed off the board than Black pieces.")
            elif self.white_pieces > self.black_pieces:
                print("Turn limit reached, White wins! More Black pieces pushed off the board than White pieces.")
            elif self.white_pieces == self.black_pieces:
                print("Turn limit reached, it's a tie! Same amount of Black and White pieces remaining.")

            print(f"Black pieces remaining: {self.black_pieces}")
            print(f"White pieces remaining: {self.white_pieces}")
            return True

    def apply_game_mode(self):
        """
        Handles the game mode selection for the player specified settings.
        """
        p1_settings = self.settings_selections["mode_p1"]
        p2_settings = self.settings_selections["mode_p2"]

        self.turn = "black"

        if p1_settings == "Computer" and p2_settings == "Computer":
            self.canvas.unbind("<Button-1>")  # unbinds mouse click event listener
            self.make_random_first_move()
            self.ai_vs_ai()

        elif p1_settings == "Computer" and p2_settings == "Human":
            self.turn = "black"
            selected_move = self.make_random_first_move()
            self.highlight_ai_move(selected_move)
            self.turn = "white"

        elif p1_settings == "Human" and p2_settings == "Human":
            # P1 color selected is only applied in the Human vs Human game mode
            if self.settings_selections["turn_color"] in (0, 1):
                self.turn = "black"
            else:
                self.turn = "white"
            self.human_vs_human = True  # disables the AI

        # only time piece selection isn't available is in AI vs AI
        if p1_settings != "Computer" or p2_settings != "Computer":
            self.canvas.bind("<Button-1>", self.click_event_listener_engine)  # sets up mouse click event listener

        # checks if game mode is changed from Human vs Human
        if p1_settings != "Human" or p2_settings != "Human":
            self.human_vs_human = False  # re-enables the AI

    def update_total_time(self):
        total_time_white = Label(self, text=f"Total Time {self.white_total_time:.2f}", bg=self.bg, font=self.font,
                                 fg=self.font_color)
        total_time_black = Label(self, text=f"Total Time {self.black_total_time:.2f}", bg=self.bg, font=self.font,
                                 fg=self.font_color)
        total_time_black.grid(row=8, column=6, padx=5)
        total_time_white.grid(row=1, column=6, padx=5)

    def draw_timer_window(self):
        """
        Initializes and draws the window containing the turn timer for both the black and white team.
        """
        font = 12
        timer_white_label = Label(self, text="White Player", bg=self.bg, font=self.font, fg=self.font_color)

        self.white_timer_box = Listbox(self, height=25, width=20, font=font)
        timer_white_label.grid(row=1, column=5, padx=5)

        self.white_timer_box.grid(row=2, column=5, rowspan=6, columnspan=1, padx=5, pady=5)
        timer_black_label = Label(self, text="Black Player", bg=self.bg, font=self.font, fg=self.font_color)

        self.black_timer_box = Listbox(self, height=25, width=20, font=font)
        timer_black_label.grid(row=8, column=5, padx=5)

        self.black_timer_box.grid(row=9, column=5, rowspan=6, columnspan=1, padx=5, pady=5)
        self.show_timer()

    def draw_moves_window(self):
        """
        Initializes the window used to display the move count of both the black and white team.
        """
        font = 12
        self.white_moves_box = Listbox(self, height=25, width=20, font=font)
        self.white_moves_box.grid(row=2, column=6, rowspan=6, columnspan=1, padx=5, pady=5)
        self.black_moves_box = Listbox(self, height=25, width=20, font=font)
        self.black_moves_box.grid(row=9, column=6, rowspan=6, columnspan=1, padx=5, pady=5)
        self.show_moves()

    def show_timer(self):
        """
        Initializes the data attribute variable to display the total time and time per move for both the black and white
        teams.
        """
        self.black_timer_box.insert(END,"Time for per move: ")
        self.white_timer_box.insert(END,"Time for per move: ")

    def show_moves(self):
        """
        Initializes the move history window within the GUI for both black and white teams.
        """
        self.white_moves_box.insert(END, "Moves:")
        self.black_moves_box.insert(END, "Moves:")

    def player_info(self):
        """
        Initializes and draws the statistics for both players, and includes the move and piece count.
        """
        font = ("Montserrat", 18, "bold")
        self.set_pieces_count()
        player_one = Label(self, text="White", bg=self.bg, font=font, fg=self.font_color)
        player_one.grid(column=2, padx=3, row=1)
        player_one_moves_label = Label(self, bg=self.bg, font=self.font,
                                       fg=self.font_color)
        player_one_moves_label.grid(column=2, row=2)
        player_one_moves_label.configure(text=f" Remaining Moves\n{self.white_move_count}")
        player_one_pieces_label = Label(self, text=f"Pieces lost\n{abs(self.white_pieces - 14)}", bg=self.bg, font=self.font,
                                        fg=self.font_color)
        player_one_pieces_label.grid(column=2, row=3)

        self.current_move_timer()

        player_two = Label(self, text="Black", bg=self.bg, font=font, fg=self.font_color)
        player_two.grid(column=4, padx=3, row=1)
        player_two_moves_label = Label(self, bg=self.bg, font=self.font,
                                       fg=self.font_color)
        player_two_moves_label.grid(column=4, row=2)
        player_two_moves_label.configure(text=f"Remaining Moves\n{self.black_move_count}")
        player_two_pieces_label = Label(self, text=f"Pieces lost\n{abs(self.black_pieces - 14)}", bg=self.bg, font=self.font,
                                        fg=self.font_color)
        player_two_pieces_label.grid(column=4, row=3)

    def current_move_timer(self):

        font = ("Montserrat", 18, "bold")
        self.current_move_timer_label = Label(self, text=f"Time:\n3:00", bg=self.bg, font=font,
                                              fg=self.font_color)
        self.current_move_timer_label.grid(column=3, row=2)

    def set_pieces_count(self):
        """
        Initializes the white and black game piece count if it hasn't been initialized.
        """
        if self.white_pieces is None and self.black_pieces is None:
            self.white_pieces = 14
            self.black_pieces = 14

    def set_move_counter(self):
        """
        Initializes the turn and game piece counter within the GUI, and draws it to the window.
        """
        try:
            self.get_settings_selections()
        except:
            if self.white_move_count is None:
                self.white_move_count = self.settings_selections['turns']
                self.black_move_count = self.settings_selections['turns']
        self.player_info()

    def create_controls(self):
        """
        Initializes and draws the buttons within the GUI.
        """
        font2 = "Montserrat", 10
        frame = Frame(self, bg=self.bg)
        start = Button(frame, text="Start", width=10, bg=self.bg, font=font2, fg=self.font_color)
        stop = Button(frame, text="Stop", width=10, bg=self.bg, font=font2, fg=self.font_color)
        pause = Button(frame, text="Pause", width=10, bg=self.bg, font=font2, fg=self.font_color)
        reset = Button(frame, text="Reset", width=10, bg=self.bg, font=font2, fg=self.font_color,
                       command=self.reset_game)
        undo = Button(frame, text="Undo Last", width=10, bg=self.bg, font=font2, fg=self.font_color, command=self.undo_last_move)
        settings = Button(frame, text="Settings", width=10, bg=self.bg, font=font2, fg=self.font_color,
                          command=self.settings_set_up)

        frame.grid(row=13, columnspan=5, sticky=W, padx=30)
        start.grid(row=13, column=2, padx=3)
        stop.grid(row=13, column=3, padx=3)
        pause.grid(row=13, column=4, padx=3)
        reset.grid(row=13, column=5, padx=3)
        undo.grid(row=13, column=6, padx=3)
        settings.grid(row=13, column=7, padx=3)

    def settings_set_up(self):
        """
        Calls the required helper methods to initialize the settings menu.
        """
        self.new_settings_window()
        self.get_settings_selections()

    def new_settings_window(self):
        """
        Calls the required helper methods to draw the settings window when the user clicks the 'Settings' buttons.
        """
        self.settings = Settings(self)
        self.settings.focus_set()
        self.settings.draw_settings()
        self.wait_window(self.settings)

    def get_settings_selections(self):
        """
        Retrieves the specified settings that the user has selected and prints it to the terminal.
        """
        self.settings_selections = self.settings.selections
        print(self.settings_selections)

        self.apply_draw_game_board_layout()
        self.white_move_count = self.settings_selections['turns']
        self.black_move_count = self.settings_selections['turns']
        self.player_info()
        self.draw_moves_window()
        self.draw_timer_window()
        self.apply_game_mode()

    def reset_game(self):
        self.apply_draw_game_board_layout()
        self.white_move_count = self.settings_selections['turns']
        self.black_move_count = self.settings_selections['turns']
        self.white_pieces = 14
        self.black_pieces = 14
        self.set_pieces_count()
        self.player_info()
        self.draw_moves_window()
        self.draw_timer_window()
        self.apply_game_mode()

    def new_game_window(self):
        """
        Performs the method calls for running the Abalone game.
        """
        self.configure(bg=self.bg)
        self.set_move_counter()
        self.create_controls()

        self.apply_draw_game_board_layout()

        self.draw_timer_window()
        self.draw_moves_window()

        self.canvas.bind("<Button-1>", self.click_event_listener_engine)  # sets up mouse click event listener

        self.mainloop()

    def update_timer(self):

        time_limit = self.settings_selections['time1']
        while time_limit > 0:
            time_limit -= 1
            self.current_move_timer_label.configure(text=time_limit)
            self.after(100, self.update_timer)


def main():
    """
    Main function for the Abalone game that acts as an entry point to run the game.
    """
    g = GameBoard()
    g.new_game_window()


if __name__ == '__main__':
    main()
