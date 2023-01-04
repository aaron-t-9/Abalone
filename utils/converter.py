class Converter:
    """
    Encapsulates helper methods for performing calculations, conversions, and game piece notation translations.
    """

    @staticmethod
    def calculate_row_length(row: int) -> int:
        """
        Calculates, and returns, the number of pieces on a given column within the game board.
        :param row: an int
        :return: an int
        """
        HEXES_PER_SIDE = 5
        HEXES_ACROSS = 2 * HEXES_PER_SIDE - 1

        if HEXES_PER_SIDE + row >= HEXES_ACROSS:
            row_length = HEXES_PER_SIDE + (HEXES_ACROSS - row) - 1
        else:
            row_length = HEXES_PER_SIDE + row
        return row_length

    @staticmethod
    def convert_row_to_string_or_int(row_val):
        """
        If provided a string representing the game board dictionary row key, then the value is converted to an int of
        the row. Else if provided an int of the row of the game board, then the int is converted into a key for the game
        board dictionary.

        :precondition row_val: a string of a key from the game_board dictionary, or an int representing a row
        :param row_val: either a string or an integer
        :return: an int if passed a string, or a string if passed an int
        """
        if type(row_val) == str:
            row_num = int(row_val.replace("row", ''))
            return row_num
        elif type(row_val) == int:
            row_key = "row" + str(row_val)
            return row_key
        else:
            print("Invalid value passed. Argument must be a string or an integer.")

    @staticmethod
    def get_opposite_color(color: str) -> str:
        """
        Gets the opposing turn_color of the turn turn_color.
        :param color: a string
        :return: a string
        """
        if color == "black":
            return "white"
        else:
            return "black"

    @staticmethod
    def calculate_column(row, col):
        """
        Calculates correct column number in game board array from given column number.

        :param row: row number: int
        :param col: column number as given: int
        :return:
        """
        rows = {
            0: 5,
            1: 4,
            2: 3,
            3: 2
        }

        if row in rows:
            col_coord = col - rows[row]
        else:
            col_coord = col - 1
        return col_coord

    @staticmethod
    def calculate_adjusted_col_direction(row_num, direction):
        """
        Calculate the coordinates of the new adjusted_direction_tuple given the current row and column of the game piece, as well as
        the adjusted_direction_tuple of movement. Required due to the varying columns on each row on the game board because of the
        hexagonal shaped game board.

        :param row_num: an int, representing the row of the selected game piece
        :param direction: a tuple, containing the new movement as (x,y) or (row, col)
        :return: an int, containing the adjusted_direction_tuple of the new movement along the column (west to east vector)
        """
        ZERO_INDEX_OFFSET = 1
        UPPER_HALF = range(0, 4 + ZERO_INDEX_OFFSET)
        MIDDLE_ROW = 4

        new_row_dir = direction[0]
        new_col_dir = direction[1]

        # if the string row_key is passed, then it is converted to an int representing the row
        if type(row_num) != int:
            row_num = Converter.convert_row_to_string_or_int(row_num)

        if row_num in UPPER_HALF:
            # checks for SE movement for pieces in the middle row
            if row_num == MIDDLE_ROW and new_row_dir == 1:
                if new_col_dir == 1:
                    new_col_dir = 0

            if row_num == MIDDLE_ROW and new_row_dir == -1:
                if new_col_dir == 1:
                    new_col_dir = 0

            # checks for NE movement
            elif new_row_dir == -1 and row_num != MIDDLE_ROW:
                if new_col_dir == 1:
                    new_col_dir = 0

            # checks for SW movement
            elif new_row_dir == 1 and row_num != MIDDLE_ROW:
                if new_col_dir == -1:
                    new_col_dir = 0

        # checks for pieces in the bottom half of the game board
        else:
            # checks for NW movement
            if new_row_dir == -1:
                if new_col_dir == -1:
                    new_col_dir = 0

            # checks for SE movement
            elif new_row_dir == 1:
                if new_col_dir == 1:
                    new_col_dir = 0

        return new_col_dir

    @staticmethod
    def calculate_adjusted_direction_tuple(row_num, direction):
        """
        Calculate the coordinates of the new adjusted_direction_tuple given the current row and column of the game piece, as well as
        the adjusted_direction_tuple of movement. Required due to the varying columns on each row on the game board because of the
        hexagonal shaped game board.

        :param row_num: an int, representing the row of the selected game piece
        :param direction: a tuple, containing the new movement as (x,y) or (row, col)
        :return: a tuple, of the adjusted_direction_tuple coordinates with the adjusted column adjusted_direction_tuple
        """
        ZERO_INDEX_OFFSET = 1
        UPPER_HALF = range(0, 4 + ZERO_INDEX_OFFSET)
        MIDDLE_ROW = 4

        new_row_dir = direction[0]
        new_col_dir = direction[1]

        # if the string row_key is passed, then it is converted to an int representing the row
        if type(row_num) != int:
            row_num = Converter.convert_row_to_string_or_int(row_num)

        if row_num in UPPER_HALF:
            # checks for SE movement for pieces in the middle row
            if row_num == MIDDLE_ROW and new_row_dir == 1:
                if new_col_dir == 1:
                    new_col_dir = 0

            if row_num == MIDDLE_ROW and new_row_dir == -1:
                if new_col_dir == 1:
                    new_col_dir = 0

            # checks for NE movement
            elif new_row_dir == -1 and row_num != MIDDLE_ROW:
                if new_col_dir == 1:
                    new_col_dir = 0

            # checks for SW movement
            elif new_row_dir == 1 and row_num != MIDDLE_ROW:
                if new_col_dir == -1:
                    new_col_dir = 0

        # checks for pieces in the bottom half of the game board
        else:
            # checks for NW movement
            if new_row_dir == -1:
                if new_col_dir == -1:
                    new_col_dir = 0

            # checks for SE movement
            elif new_row_dir == 1:
                if new_col_dir == 1:
                    new_col_dir = 0

        return new_row_dir, new_col_dir

    @staticmethod
    def get_leading_or_trailing_piece(row_num, col_num: int, num_of_adj_pieces: int, direction: tuple) -> tuple:
        """
        Gets the first (leading) or last (trailing) piece when provided the location of a specific piece along with the
        number of pieces adjacent to it, and the adjusted_direction_tuple of the vector of the adjacent pieces.

        :param row_num: a string of the row key, or an int of the row number
        :param col_num: an int of the column number
        :param num_of_adj_pieces: an int, the number of pieces adjacent to the provided piece
        :param direction: a tuple containing the adjusted_direction_tuple of movement
        :return: a tuple (str, int) where the string is the row key and the int is  the column number
        """
        if num_of_adj_pieces > 0:

            if type(row_num) != int:
                row_num = Converter.convert_row_to_string_or_int(row_num)

            row_dir = direction[0]
            col_dir = Converter.calculate_adjusted_col_direction(row_num, direction)
            for pieces in range(0, num_of_adj_pieces):
                row_num = row_num + row_dir
                col_num = col_num + col_dir

                col_dir = Converter.calculate_adjusted_col_direction(row_num, direction)

            row_key = Converter.convert_row_to_string_or_int(row_num)
            return row_key, col_num

        else:
            row_key = Converter.convert_row_to_string_or_int(row_num)
            return row_key, col_num

    @staticmethod
    def simulate_game_piece_movement(row_num, col_num: int, adjusted_direction_tuple: tuple) -> tuple:
        """
        Simulates moving the specified game piece in the specified direction, and then returns the new coordinates
        of the game piece.

        :param row_num: a string of the row key, or an int of the row number
        :param col_num: an int of the column number
        :param adjusted_direction_tuple: a tuple containing the direction of movement
        :return: a tuple (str, int) where the string is the row key and the int is  the column number
        """
        if type(row_num) != int:
            row_num = Converter.convert_row_to_string_or_int(row_num)

        row_dir = adjusted_direction_tuple[0]
        col_dir = Converter.calculate_adjusted_col_direction(row_num, adjusted_direction_tuple)

        new_row_num = row_num + row_dir
        new_col_num = col_num + col_dir

        new_row_key = Converter.convert_row_to_string_or_int(new_row_num)
        return new_row_key, new_col_num

    @staticmethod
    def external_notation_to_internal(piece: str) -> tuple:
        """
        Converts a piece from external board notation (e.g. H5) into the internal notation (e.g. '("row3, 4)).

        :param piece: string containing the piece location conforming to external board notation (e.g. 'B3')
        :return: a tuple (str, int) where the string is the row key and the int is  the column number
        """
        row_char_int_map = {
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
        try:
            row = row_char_int_map[piece[0]]
        except KeyError:
            return

        row_key = "row" + str(row)

        col = int(piece[1])
        column = Converter.calculate_column(row, col)
        return row_key, column

    @staticmethod
    def internal_notation_to_external(row_num, col_num: int) -> str:
        """
        Translates piece from internal coordinates to notation as required by game board coordinate system.

        :param row_num: a string of the row key, or an int of the row number
        :param col_num: an int of the column number
        :return: a string of the specified piece conforming to external board notation (e.g. H5)
        """
        ASCII_ALPHABET_OFFSET = 8
        ZERO_INDEX_OFFSET = 1

        TOP_ROW = 0
        UPPER_HALF = range(1, 4 + ZERO_INDEX_OFFSET)

        # if the string row_key is passed, then it is converted to an int representing the row
        if type(row_num) != int:
            row_num = Converter.convert_row_to_string_or_int(row_num)

        num_of_cols = Converter.calculate_row_length(row_num)

        if row_num == TOP_ROW:
            col_coord = num_of_cols + col_num
        elif row_num in UPPER_HALF:
            col_coord = (num_of_cols - (row_num * 2)) + col_num
        else:
            col_coord = col_num + ZERO_INDEX_OFFSET

        row_coord = chr((ASCII_ALPHABET_OFFSET - row_num) + 65)
        return row_coord + str(col_coord)
