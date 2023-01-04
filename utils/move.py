from utils.converter import Converter
from copy import deepcopy


class Move:
    """
    Encapsulates methods related to selected valid game pieces, moving selected game piece(s), or performing sumitos.
    """
    directions = [
        "NE",
        "E",
        "SE",
        "SW",
        "W",
        "NW"
    ]
    move_directions = {
        "NE": (-1, 1),
        "E": (0, 1),
        "SE": (1, 1),
        "SW": (1, -1),
        "W": (0, -1),
        "NW": (-1, -1)
    }
    opposite_directions = {
        "NE": "SW",
        "E": "W",
        "SE": "NW",
        "SW": "NE",
        "W": "E",
        "NW": "SE"
    }
    sidestep_directions = {
        "NE": ["E", "SE", "W", "NW"],
        "E": ["NE", "SE", "SW", "NW"],
        "SE": ["NE", "E", "SW", "W"],
        "SW": ["E", "SE", "W", "NW"],
        "W": ["NE", "SE", "SW", "NW"],
        "NW": ["NE", "E", "SW", "W"]
    }
    direction_tuple_map = [
        {"NE": (-1, 0), "E": (0, 1), "SE": (1, 1), "SW": (1, 0), "W": (0, -1), "NW": (-1, -1)},
        {"NE": (-1, 0), "E": (0, 1), "SE": (1, 1), "SW": (1, 0), "W": (0, -1), "NW": (-1, -1)},
        {"NE": (-1, 0), "E": (0, 1), "SE": (1, 1), "SW": (1, 0), "W": (0, -1), "NW": (-1, -1)},
        {"NE": (-1, 0), "E": (0, 1), "SE": (1, 1), "SW": (1, 0), "W": (0, -1), "NW": (-1, -1)},
        {"NE": (-1, 0), "E": (0, 1), "SE": (1, 0), "SW": (1, -1), "W": (0, -1), "NW": (-1, -1)},
        {"NE": (-1, 1), "E": (0, 1), "SE": (1, 0), "SW": (1, -1), "W": (0, -1), "NW": (-1, 0)},
        {"NE": (-1, 1), "E": (0, 1), "SE": (1, 0), "SW": (1, -1), "W": (0, -1), "NW": (-1, 0)},
        {"NE": (-1, 1), "E": (0, 1), "SE": (1, 0), "SW": (1, -1), "W": (0, -1), "NW": (-1, 0)},
        {"NE": (-1, 1), "E": (0, 1), "SE": (1, 0), "SW": (1, -1), "W": (0, -1), "NW": (-1, 0)}
    ]

    def __init__(self):
        self.direction_of_selected_pieces = None  # stores vector of selected game pieces

    def get_adj_spaces(self, row, col: int) -> set:
        """
        Gets all the game spaces adjacent to the selected game piece.
        :param row: an int, the number of the row
        :param col: an int, the number of the column
        :param num_pieces_selected: an int, the number of currently selected game pieces
        :return: a set, of the adjacent game spaces
        """
        adjacent_spaces = set()

        # if the row key is passed, then it is converted to the row number
        if type(row) != int:
            row = Converter.convert_row_to_string_or_int(row)

        # iterates through all possible directions around a given game piece
        for direction in self.directions:
            # gets the direction coordinate tuple, and gets the adjusted direction tuple
            direction_tuple = self.move_directions[direction]
            adjusted_direction_tuple = Converter.calculate_adjusted_direction_tuple(row, direction_tuple)

            # gets the internal notation of the adjacent piece
            adjacent_space_internal = Converter.simulate_game_piece_movement(row, col, adjusted_direction_tuple)

            # converts the internal notation to external notation
            adjacent_space_external = Converter.internal_notation_to_external(adjacent_space_internal[0], adjacent_space_internal[1])

            adjacent_spaces.add(adjacent_space_external)

        adjacent_spaces = self.clean_adjacent_space_set(adjacent_spaces)
        return adjacent_spaces

    def get_dir_of_selected_pieces(self, selected_pieces: list) -> list:
        """
        Gets the vector of direction of the selected game pieces
        :param selected_pieces: a list, containing the external coordinates of the selected game piece(s)
        :return: a list, containing the direction of the selected game pieces
        """
        first_piece = selected_pieces[0]
        other_piece = selected_pieces[1]  # always indexes the 2nd last piece

        # gets the row num and column number of the 1st piece
        first_piece_row_num = Converter.convert_row_to_string_or_int(first_piece[0])
        first_piece_col_num = first_piece[1]

        # gets the row num and column number of the 2nd piece
        second_piece_row_num = Converter.convert_row_to_string_or_int(other_piece[0])
        second_piece_col_num = other_piece[1]

        # gets the difference of the row number and column number between the two pieces
        row_difference = first_piece_row_num - second_piece_row_num
        col_difference = first_piece_col_num - second_piece_col_num

        # adjusts for NW movement when the 1st selected piece is North of the 2nd
        if row_difference == -1 and col_difference == 0:
            if first_piece_row_num == 4:
                col_difference = -1

        # adjusts for NE movement when the 1st selected piece is North of the 2nd
        elif row_difference == -1 and col_difference == 1:
            if first_piece_row_num == 4:
                col_difference = 0

        # adjusts for SW movement
        elif row_difference == 1 and col_difference == 0:
            if first_piece_row_num == 4:
                col_difference = -1

        # adjusts for SE movement
        elif row_difference == 1 and col_difference == 1:
            if first_piece_row_num == 4:
                col_difference = 0

        # gets the vector of direction from the direction tuple map by indexing the difference in row and column and
        # extracting the index, and getting the direction at that index
        direction_cardinal = self.get_adjusted_tuple_or_cardinal_dir(first_piece_row_num, dir_tuple=(row_difference, col_difference))

        return [direction_cardinal, self.opposite_directions[direction_cardinal]]

    def clean_adjacent_space_set(self, adjacent_spaces: set):
        """
        Removes out of bounds spaces from the adjacent spaces lIst.
        :param adjacent_spaces: a set, containing the adjacent spaces for a given piece
        :return: a set, with the out of bound spaces removed
        """
        ZERO_INDEX_OFFSET = 1
        VALID_ROWS = {"A", "B", "C", "D", "E", "F", "G", "H", "I"}
        VALID_COLS = range(0, 9 + ZERO_INDEX_OFFSET)

        temp_set = deepcopy(adjacent_spaces)
        # iterates through the spaces within adjacent spaces
        for space in temp_set:
            # gets the row and col char from each space
            row_char = space[0]
            col_char = space[1]

            # checks if the row or column is out of bounds, if so it removes it from the set of adjacent spaces
            if row_char not in VALID_ROWS or int(col_char) not in VALID_COLS:
                adjacent_spaces.remove(space)

        return adjacent_spaces

    def get_possible_single_moves(self, selected_pieces: list, num_pieces_selected: int, game_board: dict) -> set:
        """
        Gets the valid spaces for where a single selected game piece can move to. A set containing the external coords
        (e.g. H5) of valid moves to make is return.
        :param num_pieces_selected: a int, the number of currently selected game pieces
        :param selected_pieces: a list, containing the external coordinates of the selected game pieces, in order
        :param game_board: the current game board
        :return: a tuple of sets, a tuple of 2 sets.
        """
        unoccupied_game_spaces = set()

        if num_pieces_selected == 1:

            # gets the current selected game piece and converts the notation from external to internal
            selected_piece = selected_pieces[0]

            # gets all adjacent spaces to the selected piece
            adjacent_spaces = self.get_adj_spaces(selected_piece[0], selected_piece[1])

            # iterates over all adjacent spaces and filters out spaces that are occupied
            for space in adjacent_spaces:
                # converts external notation of current space on game board to internal notation
                space_internal_tuple = Converter.external_notation_to_internal(space)

                try:
                    # extracts the row key and column number from the tuple
                    row_key = space_internal_tuple[0]
                    col_num = space_internal_tuple[1]

                    adjacent_space_color = game_board[row_key][col_num]["turn_color"]

                    # means the adjacent space is unoccupied, if column number is < 0 then it is off the game board
                    if adjacent_space_color == None and col_num >= 0:
                        unoccupied_game_spaces.add(space)

                # means the adjacent space is off the game board
                except (IndexError, KeyError, TypeError):
                    pass

        return unoccupied_game_spaces

    def get_possible_grouped_moves(self, selected_pieces: list, num_pieces_selected: int, game_board: dict,
                                   turn_color: str, vector_of_dir: list) -> dict:
        """
        Gets the valid spaces for where 2 or 3 selected game pieces can move to. A dictionary containing the external
        coords (e.g. H7) of the valid spaces as the key, with the value containing the type of move (inline, sidestep,
        or sumito)
        :param num_pieces_selected: a int, the number of currently selected game pieces
        :param selected_pieces: a list, containing the external coordinates of the selected game pieces, in order
        :param game_board: the current game board
        :param turn_color: a string, the current turn turn_color
        :param vector_of_dir: a list, containing the vector of direction of the selected game pieces
        :return: a dictionary
        """
        valid_moves = {}

        # gets the first and last selected piece internal coords (e.g. ('row3', 4))
        first_selected = selected_pieces[0]
        last_selected = selected_pieces[-1]

        # adds any valid or sumito moves found
        valid_moves.update(self.get_valid_inline_moves(first_selected, last_selected, game_board, turn_color, vector_of_dir))

        return valid_moves

    def get_valid_sidestep_moves(self, selected_pieces: list, num_pieces_selected: int, game_board: dict, turn_color: str, vector_of_dir: list) -> list:
        """
        Finds the valid sidestep moves and adds it to the
        :param num_pieces_selected: a int, the number of currently selected game pieces
        :param selected_pieces: a list, containing the external coordinates of the selected game pieces, in order
        :param game_board: the current game board
        :param turn_color: a string, the current turn turn_color
        :param vector_of_dir: a list, containing the vector of direction of the selected game pieces
        :return: a list
        """
        valid_sidesteps = []
        temp_grouping = []
        is_valid_move = True

        sidestep_dirs_to_check = self.sidestep_directions[vector_of_dir[0]]
        for dir in sidestep_dirs_to_check:

            for piece in selected_pieces:
                row = piece[0]
                col = piece[1]

                # gets the adjusted direction tuple and then gets the piece adjacent to the selected piece(s)
                adjusted_dir_tuple = self.get_adjusted_tuple_or_cardinal_dir(row, cardinal_dir=dir)
                adjacent_space = Converter.simulate_game_piece_movement(row, col, adjusted_dir_tuple)

                # checks if the grouping can make a valid sidestep to spaces that are unoccupied
                try:
                    if is_valid_move and game_board[adjacent_space[0]][adjacent_space[1]]["turn_color"] == None:
                        temp_grouping.append(adjacent_space)
                    else:
                        is_valid_move = False
                except (IndexError, KeyError):
                    is_valid_move = False

            # if all selected pieces have unoccupied spaces in the direction of movement, it's added as a valid sidestep
            if is_valid_move:
                valid_sidesteps.append([temp_grouping, dir])

            # resets the is_valid_move flag and resets the temp grouping for the next direction check
            is_valid_move = True
            temp_grouping = []

        return valid_sidesteps

    def get_valid_inline_moves(self, first_selected: tuple, last_selected: tuple, game_board: dict, turn_color: str, vector_of_dir: list):
        """
        Gets the two possible inline moves for 2 and 3 group pieces.
        :param first_selected: a tuple, internal coords for the first selected piece
        :param last_selected: a tuple, internal coords for the last selected piece
        :param game_board: a dictionary, of the game board
        :param turn_color: a string, of the current turn's turn_color
        :param vector_of_dir: a list, of the vector of direction of the selected game pieces
        :return: a dictionary, of the valid spaces to move inline, or perform a sumito
        """
        valid_moves = {}

        # gets the row and column number, and direction tuple for both the first and last selected game piece
        first_selected_row_num = Converter.convert_row_to_string_or_int(first_selected[0])
        first_selected_col_num = first_selected[1]
        last_selected_row_num = Converter.convert_row_to_string_or_int(last_selected[0])
        last_selected_col_num = last_selected[1]

        # get the space in front of the first and last selected piece
        first_dir_tuple = self.get_adjusted_tuple_or_cardinal_dir(first_selected_row_num, cardinal_dir=vector_of_dir[0])

        space_infront_first = Converter.simulate_game_piece_movement(first_selected_row_num, first_selected_col_num, first_dir_tuple)
        space_infront_first_row_key = space_infront_first[0]
        space_infront_first_col_num = space_infront_first[1]
        # ensures column number isn't off the game board
        if space_infront_first_col_num >= 0:

            # if IndexError or KeyError is raised, then space is off the game board
            try:
                # gets the value of the space to move to
                infront_first_val = game_board[space_infront_first_row_key][space_infront_first_col_num]["turn_color"]

                # ensures that the space isn't occupied by piece of current turn turn_color
                if infront_first_val != turn_color:
                    valid_piece = Converter.internal_notation_to_external(space_infront_first_row_key,
                                                                          space_infront_first_col_num)

                    # if space is unoccupied, then it is added as an inline move
                    if infront_first_val == None:
                        valid_moves.update({valid_piece: "inline"})
                    # if space is occupied by opposing turn_color, then it is added as a sumito
                    elif infront_first_val == Converter.get_opposite_color(turn_color):
                        valid_moves.update({valid_piece: "sumito"})
            except (IndexError, KeyError):
                pass

        last_dir_tuple = self.get_adjusted_tuple_or_cardinal_dir(last_selected_row_num, cardinal_dir=vector_of_dir[1])
        space_infront_last = Converter.simulate_game_piece_movement(last_selected_row_num, last_selected_col_num,
                                                                    last_dir_tuple)
        space_infront_last_row_key = space_infront_last[0]
        space_infront_last_col_num = space_infront_last[1]
        # ensures column number isn't off the game board
        if space_infront_last_col_num >= 0:
            # if IndexError or KeyError is raised, then space is off the game board
            try:
                # gets the value of the space to move to
                infront_last_val = game_board[space_infront_last_row_key][space_infront_last_col_num]["turn_color"]

                # ensures that the space isn't occupied by piece of current turn turn_color
                if infront_last_val != turn_color:
                    valid_piece = Converter.internal_notation_to_external(space_infront_last_row_key,
                                                                          space_infront_last_col_num)

                    # if space is unoccupied, then it is added as an inline move
                    if infront_last_val == None:
                        valid_moves.update({valid_piece: "inline"})
                    # if space is occupied by opposing turn_color, then it is added as a sumito
                    elif infront_last_val == Converter.get_opposite_color(turn_color):
                        valid_moves.update({valid_piece: "sumito"})
            except (IndexError, KeyError):
                pass

        return valid_moves

    def get_adjusted_tuple_or_cardinal_dir(self, row, cardinal_dir=None, dir_tuple=None):
        """
        Gets either the cardinal direction if a direction tuple is passed, or the direction tuple if the cardinal
        direction is passed. Provides the adjusted direction if the direction tuple is return.
        :param row:
        :param cardinal_dir:
        :param dir_tuple:
        """
        if type(row) != int:
            row = Converter.convert_row_to_string_or_int(row)

        row_dir_keys = list(self.direction_tuple_map[row].keys())
        row_dir_values = list(self.direction_tuple_map[row].values())
        dir = None

        # gets the direction tuple
        if cardinal_dir == None:
            index = row_dir_values.index(dir_tuple)
            dir = row_dir_keys[index]

        # gets the cardinal direction
        elif dir_tuple == None:
            index = row_dir_keys.index(cardinal_dir)
            dir = row_dir_values[index]

        return dir
