from copy import deepcopy
from utils.converter import Converter


class StateSpaceGenerator:
    """
    Encapsulates the methods required to generate the state space at any given game state.
    """

    def __init__(self, board, turn):
        self.file_name = ''
        self.turn = turn
        self.board_text = ""
        self.possible_moves = set()
        self.possible_moves_single = set()
        self.possible_moves_double = set()
        self.possible_moves_triple = set()
        self.possible_moves_sumito = set()
        self.possible_moves_sumito_move_notation = set()
        self.possible_moves_sidestep = set()
        self.possible_moves_sidestep_move_notation = set()
        self.sumito_trailing_piece_turn_color = None
        self.sumito_leading_piece_opposing_color = None
        self.group = None
        self.game = board
        self.reset_board = None
        self.rows = {
            "I": 0,
            "H": 1,
            "G": 2,
            "F": 3,
            "E": 4,
            "D": 5,
            "C": 6,
            "B": 7,
            "A": 8
        }
        self.colors = {
            "b": "black",
            "w": "white"
        }
        self.move_directions = {
            "NE": (-1, 1),
            "E": (0, 1),
            "SE": (1, 1),
            "SW": (1, -1),
            "W": (0, -1),
            "NW": (-1, -1)
        }
        self.opposite_direction = {
            "NE": "SW",
            "E": "W",
            "SE": "NW",
            "SW": "NE",
            "W": "E",
            "NW": "SE"
        }
        self.sidestep_directions = {
            "NE": ["E", "NW"],
            "E": ["NE", "NW"],
            "SE": ["E", "NE"],
            "SW": ["E", "NW"],
            "W": ["NE", "NW"],
            "NW": ["E", "NE"]
        }
        self.updated_game_board = None  # contains the working game board
        self.states = []

    def set_player_turn(self, turn):
        """
        sets current turn
        """
        self.turn = turn

    def set_board(self, board):
        """
        sets board
        """
        self.game = board

    @staticmethod
    def simulate_game_piece_movement(row_num, col_num: int, direction: tuple) -> tuple:
        """
        Simulates moving the specified game piece in the specified adjusted_direction_tuple, and then returns the new coordinates
        of the game piece.

        :param row_num: a string of the row key, or an int of the row number
        :param col_num: an int of the column number
        :param direction: a tuple containing the adjusted_direction_tuple of movement
        :return: a tuple (str, int) where the string is the row key and the int is  the column number
        """
        row_dir = direction[0]
        col_dir = Converter.calculate_adjusted_col_direction(row_num, direction)

        if type(row_num) != int:
            row_num = Converter.convert_row_to_string_or_int(row_num)

        new_row_num = row_num + row_dir
        new_col_num = col_num + col_dir

        new_row_key = Converter.convert_row_to_string_or_int(new_row_num)
        return new_row_key, new_col_num

    def translate_test_input_to_board_notation(self):
        """
        Creates a game board array based on test input.

        :return: None
        """
        self.game.initialize_game_board_array()

        piece_list = self.board_text.split(',')
        for item in piece_list:
            row = self.rows[item[0]]
            row_key = "row" + str(row)
            col = int(item[1])
            color = self.colors[item[2]]
            column = Converter.calculate_column(row, col)
            row_list = self.game[row_key]
            row_list[column]['turn_color'] = color

    def create_piece_list_for_current_turn(self):
        """
        Iterates through the game board and calls helper methods to all possible moves given a specific board state.
        """
        # create an image of board before changes
        self.updated_game_board = deepcopy(self.game)

        for item in self.game.items():
            row_key = item[0]
            for column_detail in item[1]:
                # if "white" in column_detail.values():
                #     print(column_detail)
                if self.turn in column_detail.values():
                    self.generate_all_moves(row_key, column_detail)

    def get_sumito_num_of_adj_pieces(self, piece_color: str, row_key: str, col_num: int, direction: str,
                                     groupings=2) -> int:
        """
        Gets the number of adjacent pieces of the same turn_color passed to this method. Checks the pieces adjacent to the
        specified piece in the specified vector of adjusted_direction_tuple. The number of groups can be specified to determine if the
        method searches for 2 or 3 piece groupings.

        :param piece_color: a string, the turn_color of the adjacent pieces to get
        :param row_key: a string, containing the row of the piece to find adjacent pieces for
        :param col_num: an int, containing the column of the piece to find adjacent pieces for
        :param direction: a string of the raw cardinal adjusted_direction_tuple of movement (e.g. 'NE' or 'S')
        :param groupings: an int, the number of grouped pieces to perform a sumito, set to 2 by default
        :return: an int, the number of pieces adjacent to the groupings
        """
        row_num = Converter.convert_row_to_string_or_int(row_key)   # converts the row key to a number

        # gets the opposite adjusted_direction_tuple tuple to check for adjacent game pieces
        opposite_dir_tuple = self.move_directions[self.opposite_direction[direction]]

        # adjusts the adjusted_direction_tuple tuple
        adjusted_opposite_dir_tuple = (
            opposite_dir_tuple[0], Converter.calculate_adjusted_col_direction(row_num, opposite_dir_tuple))

        # gets the row key and the column number of the adjacent game piece to be checked
        new_row_num = adjusted_opposite_dir_tuple[0] + row_num
        new_row_key = Converter.convert_row_to_string_or_int(new_row_num)
        new_col_num = adjusted_opposite_dir_tuple[1] + col_num

        num_of_adj_pieces = 0
        # ensures column number isn't off the game board
        if new_col_num >= 0:
            try:
                # gets the turn_color of the adjacent game piece
                adj_space_piece_color = self.updated_game_board[new_row_key][new_col_num]["turn_color"]

                # checks if the adjacent game piece is the same turn_color, or else it returns 0
                if adj_space_piece_color == piece_color:
                    num_of_adj_pieces += 1
                else:
                    return num_of_adj_pieces

                # checks for the second adjacent game piece
                if groupings == 3:

                    # gets the new row and column of the second adjacent game piece
                    new_col_num = Converter.calculate_adjusted_col_direction(new_row_num, opposite_dir_tuple) + new_col_num
                    new_row_num = adjusted_opposite_dir_tuple[0] + new_row_num

                    # ensures column number isn't out of bounds
                    if new_col_num < 0:
                        raise KeyError

                    # checks if the row is out of bounds, and if so it means there isn't a second adjacent game piece
                    if new_row_num < 0:
                        return num_of_adj_pieces

                    # gets the new row key of the second adjacent game piece
                    new_row_key = Converter.convert_row_to_string_or_int(new_row_num)

                    # checks if second adjacent game piece is the same turn_color
                    adj_space_piece_color = self.updated_game_board[new_row_key][new_col_num]["turn_color"]
                    if (adj_space_piece_color == piece_color):
                        num_of_adj_pieces += 1

            except (IndexError, KeyError):
                # print("Adjacent piece check out of board area")
                return num_of_adj_pieces

        return num_of_adj_pieces

    def generate_inline_moves(self, row_key: str, column_detail: dict):
        """
        Runs the engine to find all of the possible inline moves for 2 and 3 groupings, as well as 2 and 3 grouped
        sumitos.

        :param row_key: a string containing the row (e.g. 'row4')
        :param column_detail: a dictionary containing the pieces for a row
        """
        # gets the row and column number of the game piece to generate inline moves for
        row_num = Converter.convert_row_to_string_or_int(row_key)
        col_num = column_detail['colNum']

        # gets the external notation of the game piece to be checked (e.g. "H6")
        piece = Converter.internal_notation_to_external(row_num, col_num)

        # iterates through the directions to check for each inline move
        for direction in self.move_directions:
            direction_tuple = self.move_directions.get(direction)

            # gets the row key and column number of where we want to move the game piece to
            new_row_num = Converter.convert_row_to_string_or_int(row_key) + direction_tuple[0]
            new_col_num = col_num + Converter.calculate_adjusted_col_direction(row_num, direction_tuple)
            new_row_key = Converter.convert_row_to_string_or_int(new_row_num)

            try:
                # ensures column number isn't out of bounds
                if new_col_num < 0:
                    raise KeyError

                # checks if the space we want to move to is unoccupied or if it's within the game board
                space_value = self.game[new_row_key][new_col_num]['turn_color']
                if space_value is None:
                    # piece can move
                    pieces = (piece, piece)

                    # adds the valid move for a single piece to the single move set
                    self.possible_moves_single.add(("i", pieces, direction, new_row_key, new_col_num))

                    # generates the moves for group inline moves
                    self.possible_multiple_piece_inline_groups(direction, row_key, col_num, new_row_num, new_col_num)

                # after checking for inline moves, valid sumitos are then checked here
                opposite_color = Converter.get_opposite_color(self.turn)
                if space_value == opposite_color and new_col_num >= 0:

                    # 2 group sumitos are checked first, and then 3 group sumitos
                    sumito_groupings = 2
                    while sumito_groupings < 4:

                        # gets the number of adjacent pieces of the turn turn_color
                        num_of_adj_selected_pieces = self.get_sumito_num_of_adj_pieces(self.turn, row_key, col_num,
                                                                                       direction, sumito_groupings)

                        # gets the opposite adjusted_direction_tuple to check for adjacent pieces of the opposite turn_color
                        opposite_direction = self.opposite_direction[direction]
                        opposite_direction_tuple = self.move_directions[opposite_direction]
                        num_of_adj_opposing_pieces = self.get_sumito_num_of_adj_pieces("white", new_row_key,
                                                                                       new_col_num, opposite_direction,
                                                                                       sumito_groupings)

                        # if num of adjacent pieces of current turn_color is greater than num of adjacent pieces of opposing
                        # turn_color them sumito is performed
                        if num_of_adj_selected_pieces > num_of_adj_opposing_pieces:
                            # getting row and col of space where sumito'ed piece is going to end up

                            # gets the internal coords for the leading piece of the opposing turn_color that will be sumitoed
                            leading_piece = Converter.get_leading_or_trailing_piece(new_row_num, new_col_num,
                                                                                    num_of_adj_opposing_pieces,
                                                                                    direction_tuple)

                            # gets the space that the leading piece will be sumito'ed to
                            piece_in_front_leading_piece = Converter.get_leading_or_trailing_piece(leading_piece[0],
                                                                                                   leading_piece[1], 1,
                                                                                                   direction_tuple)

                            # extracts the row key and column number of the space where
                            # the leading piece will be sumito'ed
                            space_in_front_row_key = piece_in_front_leading_piece[0]
                            piece_in_front_col_num = piece_in_front_leading_piece[1]

                            try:
                                # ensures column isn't out of bounds
                                if piece_in_front_col_num < 0:
                                    raise KeyError

                                # checks if the space in front of the leading space is un-occupied
                                if self.updated_game_board[space_in_front_row_key][piece_in_front_col_num]["turn_color"] is None:
                                    self.add_valid_sumito_to_move_set(col_num, direction, direction_tuple,
                                                                      leading_piece, num_of_adj_selected_pieces,
                                                                      opposite_direction_tuple, piece, row_num)

                            # if an IndexError is raised, that means a piece is going to be pushed off the board
                            except (IndexError, KeyError):
                                self.add_valid_sumito_to_move_set(col_num, direction, direction_tuple, leading_piece,
                                                                  num_of_adj_selected_pieces, opposite_direction_tuple,
                                                                  piece, row_num)

                        sumito_groupings += 1

            except (IndexError, KeyError):
                # print("Sumito check outside board area")
                pass

    def possible_multiple_piece_inline_groups(self, direction: str, row_key: str, col_num: int, new_row: int,
                                              new_column: int):
        """
        Finds the possible valid moves for inline moves with 2 and 3 piece groupings.

        :param direction: a string of the raw cardinal adjusted_direction_tuple of movement (e.g. 'NE' or 'S')
        :param row_key: a string of the row key
        :param col_num: an int of the column number
        :param new_row: an int of the row of the desired space to move to
        :param new_column: an int of the new column of desired space to move to
        """
        selected_row_num = Converter.convert_row_to_string_or_int(row_key) # converts the row key to a number

        # gets the tuple of the opposite adjusted_direction_tuple
        opposite_dir = self.opposite_direction.get(direction)
        opposite_dir_tuple = self.move_directions[opposite_dir]

        adjusted_new_row_num = selected_row_num + opposite_dir_tuple[0]
        adjusted_piece_row_key = Converter.convert_row_to_string_or_int(adjusted_new_row_num)
        adjusted_piece_col_num = col_num + Converter.calculate_adjusted_col_direction(selected_row_num, opposite_dir_tuple)

        if self.is_valid_adjacent_piece(adjusted_piece_row_key, adjusted_piece_col_num):

            # gets the external notation for the leading and last game piece (e.g. H6)
            leading_piece_coords = Converter.internal_notation_to_external(selected_row_num, col_num)
            trailing_piece_coords = Converter.internal_notation_to_external(adjusted_new_row_num, adjusted_piece_col_num)

            pieces = (leading_piece_coords, trailing_piece_coords)
            new_row_key = Converter.convert_row_to_string_or_int(new_row)

            self.possible_moves_double.add(("i", pieces, direction, new_row_key, new_column))

            # Checks for 3-piece move groups
            # ----------------------------------------------------------------------------------------------------
            adjusted_piece_col_num = adjusted_piece_col_num + Converter.calculate_adjusted_col_direction(adjusted_new_row_num, opposite_dir_tuple)

            adjusted_new_row_num = adjusted_new_row_num + opposite_dir_tuple[0]
            adj_piece_row_key = Converter.convert_row_to_string_or_int(adjusted_new_row_num)

            if self.is_valid_adjacent_piece(adj_piece_row_key, adjusted_piece_col_num):
                leading_piece_coords = Converter.internal_notation_to_external(selected_row_num, col_num)
                trailing_piece_coords = Converter.internal_notation_to_external(adjusted_new_row_num, adjusted_piece_col_num)

                pieces = (leading_piece_coords, trailing_piece_coords)
                new_row_key = Converter.convert_row_to_string_or_int(new_row)

                self.possible_moves_triple.add(("i", pieces, direction, new_row_key, new_column))

    def add_valid_sumito_to_move_set(self, col_num: int, direction: str, direction_tuple: tuple, leading_piece: tuple,
                                     num_of_adj_selected_pieces: int, opposite_direction_tuple: tuple, piece: str,
                                     row_num: int):
        """
        Helper method containing the logic to perform the sumito. Adds the type of move, the pieces involved in the
        sumito, the adjusted_direction_tuple of movement, as well as the internal board coordinates of game board space the movement
        is going to occur. Also generates the move notation for sumitos.

        :param col_num: a int, of the column number of the selected piece
        :param direction: a string of the raw cardinal adjusted_direction_tuple (e.g. 'NE', 'W')
        :param direction_tuple: a tuple containing the coordinates of the adjusted_direction_tuple of movement (e.g. '(-1, 1)')
        :param leading_piece: a tuple containing the internal coordinates of the leading piece
        :param num_of_adj_selected_pieces: an int of the number of pieces adjacent to the selected piece
        :param opposite_direction_tuple: a tuple containing the coordinates of the opposite adjusted_direction_tuple of movement
        :param piece: a str of the selected piece in external board notatation (e.g. 'G3')
        :param row_num: an int
        :return:
        """
        # gets the turn_color of the leading game piece that will be sumito'ed
        leading_piece_color = self.updated_game_board[leading_piece[0]][leading_piece[1]]["turn_color"]
        if leading_piece_color != self.turn:

            # gets the internal coordinates of the trailing piece of the turn turn_color
            trailing_piece = Converter.get_leading_or_trailing_piece(row_num, col_num, num_of_adj_selected_pieces,
                                                                     opposite_direction_tuple)

            # extracts the row number and column number of the leading piece that will be sumito'ed
            leading_piece_row_num = Converter.convert_row_to_string_or_int(leading_piece[0])
            leading_piece_col_num = leading_piece[1]
            # gets the space that the leading game piece wil lbe sumito'ed to
            empty_space_coords = self.simulate_game_piece_movement(leading_piece_row_num, leading_piece_col_num,
                                                                   direction_tuple)

            # converts the notation of the leading piece from internal to external notation (e.g. H6)
            leading_piece = Converter.internal_notation_to_external(leading_piece[0], leading_piece[1])

            # gets the space that the piece behind the leading piece will move to
            second_place_piece = self.simulate_game_piece_movement(leading_piece_row_num, leading_piece_col_num,
                                                                   opposite_direction_tuple)
            # converts the notation of the second place piece from internal to external (e.g. H6)
            second_place_piece = Converter.internal_notation_to_external(second_place_piece[0], second_place_piece[1])

            # converts the notation of the last piece from internal to external (e.g. H6)
            trailing_piece = Converter.internal_notation_to_external(trailing_piece[0], trailing_piece[1])

            # packs the leading piece, second place piece, and the last piece into a tuple
            pieces = (leading_piece, second_place_piece, trailing_piece)
            # adds the legal sumito move to the possible move notation to be written to the .board file
            self.possible_moves_sumito.add(("i", pieces, direction, empty_space_coords[0], empty_space_coords[1]))


            move_notation_pieces = (piece, trailing_piece)
            # adds the legal sumito move to the set conforming to our move notation to be written to the .moves file
            self.possible_moves_sumito_move_notation.add(
                ("i", move_notation_pieces, direction, empty_space_coords[0], empty_space_coords[1]))

    def is_valid_adjacent_piece(self, opposite_adj_row_key: str, opposite_adj_col_num: int) -> bool:
        """
        Checks if the piece behind is of the same turn_color, and returns a true if it is, or else false is returned.

        :param opposite_adj_col_num: a string of row_key of the adjacent piece to be checked
        :param opposite_adj_row_key: an int, of the column of the adjacent piece to be checked
        :return: a boolean
        """

        # checks if the adjacent piece in the opposing adjusted_direction_tuple of movement is the same turn_color as the select piece
        try:
            # ensures column isn't out of bounds
            if opposite_adj_col_num < 0:
                raise KeyError

            if self.updated_game_board[opposite_adj_row_key][opposite_adj_col_num]["turn_color"] == self.turn:
                return True
            else:
                return False

        except (IndexError, KeyError):
            # print("Adjacent 2nd piece out of board area")
            return False

    def generate_all_moves(self, row_key: str, column_detail: dict):
        self.generate_inline_moves(row_key, column_detail)
        self.generate_sidestep_moves(row_key, column_detail)
        self.possible_moves.union(self.possible_moves_single).union(self.possible_moves_double) \
            .union(self.possible_moves_triple).union(self.possible_moves_sumito_move_notation) \
            .union(self.possible_moves_sidestep)

    def generate_sidestep_moves(self, row_key: str, column_detail: dict):
        """
        Generates and finds all legal sidestep moves for a given board state.

        :param row_key: a string containing the row (e.g. 'row4')
        :param column_detail: a dictionary containing the pieces for a row
        """
        row_num = Converter.convert_row_to_string_or_int(row_key)
        col_num = column_detail['colNum']
        piece = Converter.internal_notation_to_external(row_num, col_num)

        for direction in self.move_directions:
            direction_tuple = self.move_directions.get(direction)

            new_row_num = Converter.convert_row_to_string_or_int(row_key) + direction_tuple[0]
            new_col_num = col_num + Converter.calculate_adjusted_col_direction(row_num, direction_tuple)
            new_row_key = Converter.convert_row_to_string_or_int(new_row_num)

            # if there isn't a valid 2 group sidestep, then skip_dir tells the method
            # to skip checking for a 3 piece sidestep for the same direction
            skip_dir = None

            try:
                # ensures column isn't out of boudns
                if new_col_num < 0:
                    raise KeyError

                space_value = self.game[new_row_key][new_col_num]['turn_color']
                if space_value is None and new_col_num >= 0:

                    # sets the grouping of sidesteps to find possible moves for
                    sidestep_groupings = 2
                    while sidestep_groupings < 4:

                        # gets the complimentary sidesteps directions to check for
                        sidestep_dirs_to_check = self.sidestep_directions[direction]
                        for sidestep_complimentary_dir in sidestep_dirs_to_check:
                            num_of_adj_pieces = self.get_sidestep_num_of_adj_pieces(self.turn, row_key, col_num,
                                                                                    sidestep_complimentary_dir,
                                                                                    sidestep_groupings)

                            if num_of_adj_pieces > 0:
                                # gets the sidestep move adjusted_direction_tuple coords
                                sidestep_complimentary_dir_tuple = self.move_directions[sidestep_complimentary_dir]

                                adj_piece_row = row_num
                                adj_piece_col = col_num
                                adj_piece_coords = self.simulate_game_piece_movement(adj_piece_row, adj_piece_col,
                                                                                     sidestep_complimentary_dir_tuple)

                                # checks all of the adjacent pieces to see if they are able to perform a sidestep
                                for adj_piece in range(0, num_of_adj_pieces):
                                    # gets the coords of the adjacent piece
                                    adj_piece_coords = self.simulate_game_piece_movement(adj_piece_row, adj_piece_col,
                                                                                         sidestep_complimentary_dir_tuple)

                                    adj_piece_row = adj_piece_coords[0]
                                    adj_piece_col = adj_piece_coords[1]

                                # gets trailing piece and converts it to external board notation (e.g. H6)
                                trailing_piece = Converter.internal_notation_to_external(adj_piece_coords[0],
                                                                                         adj_piece_coords[1])

                                # checks if the adjacent piece can make a sidestep
                                sidestep_space = self.simulate_game_piece_movement(adj_piece_row, adj_piece_col,
                                                                                   direction_tuple)

                                # checks if the space that the adjacent piece wants to sidestep to is empty, and that the space to move to is within the game board
                                try:

                                    # ensures column isn't out of bounds
                                    if sidestep_space[1] < 0:
                                        raise KeyError

                                    if self.updated_game_board[sidestep_space[0]][sidestep_space[1]]["turn_color"] is None and sidestep_complimentary_dir != skip_dir:

                                        # handles adding 3 group side steps to the move list
                                        if num_of_adj_pieces == 2:
                                            # gets middle piece and converts it to external board notation (e.g. H6)
                                            middle_piece_tuple = self.simulate_game_piece_movement(row_num, col_num,
                                                                                                   sidestep_complimentary_dir_tuple)
                                            middle_piece = Converter.internal_notation_to_external(
                                                middle_piece_tuple[0], middle_piece_tuple[1])

                                            # add pieces to a tuple and adds the move into the sidestep moves set
                                            pieces = (piece, middle_piece, trailing_piece)
                                            self.possible_moves_sidestep.add(
                                                ("s", pieces, direction, new_row_key, new_col_num))

                                            # add pieces to the move notation set
                                            pieces_move_notation = (piece, trailing_piece)
                                            self.possible_moves_sidestep_move_notation.add(
                                                ("s", pieces_move_notation, direction, new_row_key, new_col_num))

                                        # handles adding 2 group side steps to the move list
                                        elif num_of_adj_pieces == 1:
                                            adj_piece_board_notation = Converter.internal_notation_to_external(
                                                adj_piece_row, adj_piece_col)
                                            pieces = (piece, adj_piece_board_notation)
                                            self.possible_moves_sidestep.add(
                                                ("s", pieces, direction, new_row_key, new_col_num))

                                            # adds the pieces to the move notation set
                                            pieces_move_notation = (piece, adj_piece_board_notation)
                                            self.possible_moves_sidestep_move_notation.add(
                                                ("s", pieces_move_notation, direction, new_row_key, new_col_num))
                                    else:
                                        # if there isn't a valid 2 group sidestep, then skip_dir tells the method
                                        # to skip checking for a 3 piece sidestep for the same direction
                                        skip_dir = sidestep_complimentary_dir

                                except (IndexError, KeyError):
                                    pass

                        sidestep_groupings += 1

            except (IndexError, KeyError):
                pass

    def get_sidestep_num_of_adj_pieces(self, piece_color: str, row_key: str, col_num: int, direction: str, groupings=2):
        """
        Finds the number of adjacent pieces that can make a legal sidestep move.

        :param piece_color: a string, the turn_color of the adjacent pieces to get
        :param row_key: a string, containing the row key (e.g. 'row3')
        :param col_num: an int, containing the column number
        :param direction: a string of the raw caridnal adjusted_direction_tuple (e.g. 'NE' or 'W')
        :param groupings: an int, the number of grouped pieces to search for, set to 2 by default
        :return: an int, the number of pieces adjacent to the specified piece
        """
        row_num = Converter.convert_row_to_string_or_int(row_key)   # converts row key to a number
        dir_tuple = self.move_directions[direction]    # gets the tuple of adjusted_direction_tuple

        # adjusts the adjusted_direction_tuple tuple
        adjusted_dir_tuple = (dir_tuple[0], Converter.calculate_adjusted_col_direction(row_num, dir_tuple))

        # gets the row key and column number of the adjacent piece
        new_row_num = adjusted_dir_tuple[0] + row_num
        new_row_key = Converter.convert_row_to_string_or_int(new_row_num)
        new_col_num = adjusted_dir_tuple[1] + col_num

        num_of_adj_pieces = 0
        try:

            # ensures column isn't out of bounds
            if new_col_num < 0:
                raise KeyError

            # gets the turn_color of the adjacent piece
            adj_space_piece_color = self.updated_game_board[new_row_key][new_col_num]["turn_color"]

            # checks if adjacent piece is same turn_color or else it returns 0
            if adj_space_piece_color == piece_color:
                num_of_adj_pieces += 1
            else:
                return num_of_adj_pieces

            if groupings == 3:
                new_col_num = Converter.calculate_adjusted_col_direction(new_row_num, dir_tuple) + new_col_num
                new_row_num = adjusted_dir_tuple[0] + new_row_num

                # checks if the row is out of bounds, and if so it means there isn't a second adjacent game piece
                if new_row_num < 0:
                    return num_of_adj_pieces

                # gets the row key for the second adjacent game piece
                new_row_key = Converter.convert_row_to_string_or_int(new_row_num)

                # checks if second adjacent game piece is the same turn_color
                adj_space_piece_color = self.updated_game_board[new_row_key][new_col_num]["turn_color"]
                if adj_space_piece_color == piece_color:
                    num_of_adj_pieces += 1

        except (IndexError, KeyError):
            # print("Adjacent piece check out of board area")
            return num_of_adj_pieces

        return num_of_adj_pieces

    def update_board(self):
        """
        Contains for-loops to iterate over the sets of different types of moves, updates the board state for each move,
        and writes the board state to a .board file.
        """

        for move in self.possible_moves_sumito:
            # only for single piece moves
            if move[0] == 'i':

                leading_piece_coords = Converter.external_notation_to_internal(move[1][0])
                second_place_piece_coords = Converter.external_notation_to_internal(move[1][1])
                trailing_piece_coords = Converter.external_notation_to_internal(move[1][2])

                opposing_color = Converter.get_opposite_color(self.turn)
                color_of_second_piece = \
                    self.updated_game_board[second_place_piece_coords[0]][second_place_piece_coords[1]]["turn_color"]

                try:
                    # ensures column number isn't out of bounds
                    if move[4] < 0:
                        raise KeyError

                    # push opposing piece
                    self.updated_game_board[move[3]][move[4]]["turn_color"] = opposing_color

                except (IndexError, KeyError):
                    # shift pieces as piece has been pushed off game board
                    sumitoed_piece = Converter.internal_notation_to_external(leading_piece_coords[0],
                                                                             leading_piece_coords[1])

                    # print(f"{sumitoed_piece + opposing_color[0]} pushed off the board!")

                finally:
                    # leading piece replaced by turn_color of piece directly behind it
                    self.updated_game_board[leading_piece_coords[0]][leading_piece_coords[1]][
                        "turn_color"] = color_of_second_piece

                    # replaces second place piece with piece of turn turn_color
                    self.updated_game_board[second_place_piece_coords[0]][second_place_piece_coords[1]][
                        "turn_color"] = self.turn

                    # removes trailing piece
                    self.updated_game_board[trailing_piece_coords[0]][trailing_piece_coords[1]]["turn_color"] = None

                # self.output_board()
                self.states.append([move, self.updated_game_board])
                # resets board to before move
                self.updated_game_board = deepcopy(self.game)

        for move in self.possible_moves_triple:
            # only for single piece moves
            if move[0] == 'i':
                # move trailing piece up front
                self.updated_game_board[move[3]][move[4]]["turn_color"] = self.turn

                trailing_piece_external_coords = move[1][1]
                trailing_piece_coords = self.translate_external_coords_to_internal_coords(
                    trailing_piece_external_coords)
                # remove old trailing piece
                self.updated_game_board[trailing_piece_coords[0]][trailing_piece_coords[1]]["turn_color"] = None
                #self.output_board()
                # resets board to before move
                self.states.append([move, self.updated_game_board])
                self.updated_game_board = deepcopy(self.game)

        for move in self.possible_moves_double:
            # only for single piece moves
            if move[0] == 'i':
                # move trailing piece up front
                self.updated_game_board[move[3]][move[4]]["turn_color"] = self.turn

                trailing_piece_external_coords = move[1][1]
                trailing_piece_coords = self.translate_external_coords_to_internal_coords(
                    trailing_piece_external_coords)
                # remove old trailing piece
                self.updated_game_board[trailing_piece_coords[0]][trailing_piece_coords[1]]["turn_color"] = None
                #self.output_board()
                # resets board to before move
                self.states.append([move, self.updated_game_board])
                self.updated_game_board = deepcopy(self.game)

        for move in self.possible_moves_sidestep:

            piece_sidestep_list = move[1]
            direction = move[2]
            direction_tuple = self.move_directions[direction]
            for piece in piece_sidestep_list:
                piece_coords_tuple = self.translate_external_coords_to_internal_coords(piece)

                # removes where the piece used to be
                self.updated_game_board[piece_coords_tuple[0]][piece_coords_tuple[1]]["turn_color"] = None

                # gets the adjusted_direction_tuple of the side step and packs the adjusted_direction_tuple into a tuple
                sidestep_row_dir_coord = direction_tuple[0]
                sidestep_col_dir_coord = Converter.calculate_adjusted_col_direction(piece_coords_tuple[0],
                                                                                    direction_tuple)
                sidestep_dir_tuple = (sidestep_row_dir_coord, sidestep_col_dir_coord)

                # performs the sidestep
                sidestep_piece = self.simulate_game_piece_movement(piece_coords_tuple[0], piece_coords_tuple[1],
                                                                   sidestep_dir_tuple)
                self.updated_game_board[sidestep_piece[0]][sidestep_piece[1]]["turn_color"] = self.turn

            #self.output_board()
            self.states.append([move, self.updated_game_board])
            # resets board to before move
            self.updated_game_board = deepcopy(self.game)

        for move in self.possible_moves_single:
            # only for single piece moves
            if move[0] == 'i':
                # move front piece up
                self.updated_game_board[move[3]][move[4]]['turn_color'] = self.turn
                # remove back piece
                location = Converter.external_notation_to_internal(move[1][1])
                self.updated_game_board[location[0]][location[1]]['turn_color'] = None
                #self.output_board()
                # resets board to before move
                self.states.append([move, self.updated_game_board])
                self.updated_game_board = deepcopy(self.game)


    def translate_external_coords_to_internal_coords(self, piece_coord: str) -> tuple:
        """
        Provided piece notation in the format of external coordinates (e.g. 'H4'), it converts the coordinates to
        internal board coordinates.

        :param piece_coord: a string, external board coordinates used to represent a piece (e.g. 'H5')
        :return: a tuple, (str, int), where the string is the row key, e.g. "row3", and the int is the column number
        """
        ASCII_OFFSET = 65
        NUM_OF_ROWS_OFFSET = 8

        row_letter = piece_coord[0]

        row_num = (ord(row_letter) - ASCII_OFFSET - NUM_OF_ROWS_OFFSET) * -1
        col_num = Converter.calculate_column(row_num, int(piece_coord[1]))

        if row_num < 0:
            # print("Out of range coordinates passed to translate_external_coords_to_internal_coords")
            pass

        row_key = Converter.convert_row_to_string_or_int(row_num)
        return row_key, col_num

    def read_test_input(self):
        """
        Reads test input and sets the board and turn.
        """
        colors = {
            "b": "black",
            "w": "white"
        }
        with open(f"{self.file_name}.input", 'r') as input_file:
            self.turn = colors[input_file.readline().replace('\n', '')]
            self.board_text = input_file.readline()

    def output_board(self):
        """
        Given the current board state, it generates a list containing the positions of the black and white game pieces
        and calls a helper method to write these lists to a text file.
        """
        blacks = []
        whites = []

        for row, col in self.updated_game_board.items():
            for piece in col:

                if piece["turn_color"] is not None:

                    row_num = Converter.convert_row_to_string_or_int(row)
                    col_num = piece["colNum"]
                    piece_letter_coord = Converter.internal_notation_to_external(row_num, col_num)

                    if piece["turn_color"] == "black":
                        blacks.append(piece_letter_coord + 'b')
                    else:
                        whites.append(piece_letter_coord + 'w')

        self.print_to_text_file(sorted(blacks) + sorted(whites))

    def text_output_moves(self):
        """
        Outputs move in move notation conforming to the move notation provided.
        """
        with open(f"{self.file_name}.moves", "a") as file:
            for i in self.possible_moves:
                move_type = i[0]
                pieces = i[1]
                direction = i[2]
                item = f"{move_type}-{pieces[0]}-{pieces[1]}-{direction}"
                file.write(item)
                file.write("\n")

    def print_to_text_file(self, item: list):
        """
        Writes the list containing the black and white game pieces for any given board game state to a text file with
        a .board file extension.

        :param item: a list, containing the black and white pieces on any given board game state
        :return:
        """
        item = str(item)
        item = item.replace('[', '').replace(']', '').replace(' ', '').replace("'", '')
        with open(f"{self.file_name}.board", "a") as file:
            file.write(item)
            file.write("\n")

    def run_tests(self):
        """
        Main method to call helper methods to run the state space generator.
        """
        self.read_test_input()
        self.translate_test_input_to_board_notation()
        self.create_piece_list_for_current_turn()
        self.update_board()
        self.text_output_moves()

    def run_generation(self):
        self.create_piece_list_for_current_turn()
        self.update_board()
        return self.states


# def main():
#     """
#     Main function for the statespace generator tests.
#     """
#     s = StateSpaceGenerator()
#     # TODO need to make this take a real game board and or call from game rather than in this main function
#     # for input file testing
#     s.file_name = sys.argv[1].split('.')[0]
#     s.run_tests()
#
#
# if __name__ == '__main__':
#     main()
#
