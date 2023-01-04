from utils.converter import *

test_board = {'row0': [{'colNum': 0, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 1, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 2, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 3, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 4, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None}],
              'row1': [{'colNum': 0, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 1, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 2, 'turn_color': 'black', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 3, 'turn_color': 'white', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 4, 'turn_color': 'white', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 5, 'turn_color': 'white', 'selected': False, 'x_pos': None, 'y_pos': None}],
              'row2': [{'colNum': 0, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 1, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 2, 'turn_color': 'white', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 3, 'turn_color': 'black', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 4, 'turn_color': 'white', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 5, 'turn_color': 'white', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 6, 'turn_color': 'white', 'selected': False, 'x_pos': None, 'y_pos': None}],
              'row3': [{'colNum': 0, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 1, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 2, 'turn_color': 'white', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 3, 'turn_color': 'black', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 4, 'turn_color': 'black', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 5, 'turn_color': 'black', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 6, 'turn_color': 'black', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 7, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None}],
              'row4': [{'colNum': 0, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 1, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 2, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 3, 'turn_color': 'black', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 4, 'turn_color': 'black', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 5, 'turn_color': 'black', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 6, 'turn_color': 'white', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 7, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 8, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None}],
              'row5': [{'colNum': 0, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 1, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 2, 'turn_color': 'white', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 3, 'turn_color': 'white', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 4, 'turn_color': 'black', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 5, 'turn_color': 'white', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 6, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 7, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None}],
              'row6': [{'colNum': 0, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 1, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 2, 'turn_color': 'white', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 3, 'turn_color': 'white', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 4, 'turn_color': 'black', 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 5, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 6, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None}],
              'row7': [{'colNum': 0, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 1, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 2, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 3, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 4, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 5, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None}],
              'row8': [{'colNum': 0, 'turn_color': "black", 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 1, 'turn_color': "black", 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 2, 'turn_color': None, 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 3, 'turn_color': "black", 'selected': False, 'x_pos': None, 'y_pos': None},
                       {'colNum': 4, 'turn_color': "black", 'selected': False, 'x_pos': None, 'y_pos': None}]}
turn = "black"


def center(board, color):
    """
    gets average of distance from center of all pieces of provided turn_color
    :param board: gameboard array
    :param color: player whose turn it is turn_color
    :return: float
    """
    distance = {
        4: [(0, 4), (1, 5), (2, 6), (3, 7), (4, 8), (5, 7), (6, 6), (7, 5)],
        3: [(2, 5), (3, 6), (4, 7), (5, 6), (6, 5)],
        2: [(3, 5), (4, 6), (5, 5)],
        1: [(4,5)]
    }
    proximity_counter = 0
    pieces = 0
    # 9 rows 9 columns center is E5 or board notation row 4 column 4
    for row in board.items():
        row_number = Converter.convert_row_to_string_or_int(row[0])
        row = row[1]
        for place in row:
            if place['turn_color'] == color:
                pieces += 1
                column = place['colNum']
                dist = 0
                if row_number == 0 or row_number == 8 or column == 0 or (row_number, column) in distance[4]:
                    dist = 4
                elif row_number == 1 or row_number == 7 or column == 1 or (row_number, column) in distance[3]:
                    dist = 3
                elif row_number == 2 or row_number == 6 or column == 2 or (row_number, column) in distance[2]:
                    dist = 2
                elif row_number == 3 or row_number == 5 or column == 3 or (row_number, column) in distance[1]:
                    dist = 1
                proximity_counter += dist
    proximity_counter = proximity_counter/pieces
    return proximity_counter


def pieces(board, color):
    """
    counts pieces of the turn_color on the board
    :param board: gameboard array
    :param color: player whose turn it is turn_color
    :return: int
    """
    piece_count = 0
    for row in board.items():
        row = row[1]
        for place in row:
            if place['turn_color'] == color:
                piece_count += 1
    return piece_count


def groups(board: dict, turn_color: str) -> list:
    """
    Returns the ally count of the specified color for a given game board state.
    :param board: a dictionary, of the game board
    :param turn_color: a string, the color to perform the ally count for
    :return: a list of lists, containing the ally count groupings
    """
    ally_count = []  # contains all of the groupings of ally counts
    ally_count_grouping = []  # temporarily stores the current ally count grouping
    neighbours_to_check = set()
    already_checked = set()

    for row in board:
        for piece in board[row]:

            if piece["turn_color"] == turn_color and (row, piece["colNum"]) not in already_checked:

                ally_count_grouping.append((row, piece["colNum"]))  # adds the piece to the ally count grouping
                already_checked.add((row, piece["colNum"]))  # adds the piece to the set of already checked pieces
                neighbours_to_check.add((row, piece["colNum"]))

                # checks the all neighbours of the piece, and neighbours of neighbours of neighbours...etc
                valid_neighbours = True
                while valid_neighbours:
                    piece_to_check = neighbours_to_check.pop()
                    adjacent_pieces = get_adj_spaces_in_internal_notation(piece_to_check[0], piece_to_check[1])  # gets adjacent pieces

                    for adjacent_piece in adjacent_pieces:
                        try:
                            if board[adjacent_piece[0]][adjacent_piece[1]]["turn_color"] == turn_color and adjacent_piece not in already_checked:

                                ally_count_grouping.append(adjacent_piece)
                                already_checked.add(adjacent_piece)
                                neighbours_to_check.add(adjacent_piece)

                        except IndexError:
                            pass

                    if len(neighbours_to_check) == 0:
                        ally_count.append(ally_count_grouping)  # adds the grouping to the ally count
                        valid_neighbours = False

                ally_count_grouping = []  # resets the list containing the current ally count grouping

    return ally_count


def get_adj_spaces_in_internal_notation(row, col: int) -> set:
    """
    Gets all the game spaces adjacent to the selected game piece.
    :param row: an int, the number of the row
    :param col: an int, the number of the column
    :param num_pieces_selected: an int, the number of currently selected game pieces
    :return: a set, of the adjacent game spaces
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
    adjacent_spaces = set()

    # if the row key is passed, then it is converted to the row number
    if type(row) != int:
        row = Converter.convert_row_to_string_or_int(row)

    # iterates through all possible directions around a given game piece
    for dir in directions:
        # gets the direction coordinate tuple, and gets the adjusted direction tuple
        direction_tuple = move_directions[dir]
        adjusted_direction_tuple = Converter.calculate_adjusted_direction_tuple(row, direction_tuple)

        # gets the internal notation of the adjacent piece
        adjacent_space_internal = Converter.simulate_game_piece_movement(row, col, adjusted_direction_tuple)

        if is_in_bounds(adjacent_space_internal[0], adjacent_space_internal[1]):
            adjacent_spaces.add(adjacent_space_internal)

    return adjacent_spaces


def is_in_bounds(row, col: int) -> bool:
    """
    Checks if the given coordinates is within the game board
    :param row: an int or string, of the row
    :param col: an int, of the colujn
    :return: a boolean, if the coordinates are within the game board
    """
    NUM_COLS_PER_ROW = [
        5,
        6,
        7,
        8,
        9,
        8,
        7,
        6,
        5
    ]
    VALID_ROWS_COLS = range(0, 9)

    if type(row) != int:
        row = Converter.convert_row_to_string_or_int(row)

    if row in VALID_ROWS_COLS and col in VALID_ROWS_COLS:

        COLS_PER_ROW = NUM_COLS_PER_ROW[row]  # gets num of columns for the given row
        if col in range(0, COLS_PER_ROW):  # checks if the column is in bounds for that row
            return True
    else:
        return False


def space_translation(board, adj_list, color):
    """
    finds any same turn_color adjacent pieces to the current piece
    :param board:
    :param adj_list:
    :param color:
    :return:
    """
    adjs = []
    for item in adj_list:
        spot = Converter.external_notation_to_internal(item)
        for item in board[spot[0]]:
            if item['colNum'] == spot[1]:
                if item['turn_color'] == color:
                    adjs.append(spot)


def push_eval(state, center_val):

    move = state[0]

    # gets color of leading piece within piece notation, cause within our notation, the lead piece in the Move
    # is the opposing color (e.g. move[1][0] will be the opposite color for a sumito)
    internal_notation = Converter.external_notation_to_internal(move[1][0])
    color_of_lead_piece_in_move_notation = state[1][internal_notation[0]][internal_notation[1]]["turn_color"]

    if len(move[1]) == 3 and color_of_lead_piece_in_move_notation != state[2] and color_of_lead_piece_in_move_notation is not None:
        push = True
    else:
        push = False

    if push:
        total = 5 - center_val
        #print("total", total)
        if total < 4.8:
            return 0.5
        else:
            return 5
    else:
        return 0


class AllyCount:

    def __init__(self):
        self.ally_groups = []  # contains sets with the ally counts
        self.game_board = {}


test_state = (('i', ('C4', 'C5', 'C6'), 'W', 'row6', 2), {'row0': [{'colNum': 0, 'turn_color': 'white', 'selected': False, 'x_pos': 240, 'y_pos': 57}, {'colNum': 1, 'turn_color': 'white', 'selected': False, 'x_pos': 295, 'y_pos': 57}, {'colNum': 2, 'turn_color': None, 'selected': False, 'x_pos': 350, 'y_pos': 57}, {'colNum': 3, 'turn_color': None, 'selected': False, 'x_pos': 405, 'y_pos': 57}, {'colNum': 4, 'turn_color': None, 'selected': False, 'x_pos': 460, 'y_pos': 57}], 'row1': [{'colNum': 0, 'turn_color': 'white', 'selected': False, 'x_pos': 212, 'y_pos': 104}, {'colNum': 1, 'turn_color': 'white', 'selected': False, 'x_pos': 267, 'y_pos': 104}, {'colNum': 2, 'turn_color': 'white', 'selected': False, 'x_pos': 322, 'y_pos': 104}, {'colNum': 3, 'turn_color': None, 'selected': False, 'x_pos': 377, 'y_pos': 104}, {'colNum': 4, 'turn_color': None, 'selected': False, 'x_pos': 432, 'y_pos': 104}, {'colNum': 5, 'turn_color': 'white', 'selected': False, 'x_pos': 487, 'y_pos': 104}], 'row2': [{'colNum': 0, 'turn_color': None, 'selected': False, 'x_pos': 185, 'y_pos': 152}, {'colNum': 1, 'turn_color': None, 'selected': False, 'x_pos': 240, 'y_pos': 152}, {'colNum': 2, 'turn_color': None, 'selected': False, 'x_pos': 295, 'y_pos': 152}, {'colNum': 3, 'turn_color': None, 'selected': False, 'x_pos': 350, 'y_pos': 152}, {'colNum': 4, 'turn_color': 'white', 'selected': False, 'x_pos': 405, 'y_pos': 152}, {'colNum': 5, 'turn_color': 'white', 'selected': False, 'x_pos': 460, 'y_pos': 152}, {'colNum': 6, 'turn_color': 'black', 'selected': False, 'x_pos': 515, 'y_pos': 152}], 'row3': [{'colNum': 0, 'turn_color': None, 'selected': False, 'x_pos': 157, 'y_pos': 200}, {'colNum': 1, 'turn_color': None, 'selected': False, 'x_pos': 212, 'y_pos': 200}, {'colNum': 2, 'turn_color': 'white', 'selected': False, 'x_pos': 267, 'y_pos': 200}, {'colNum': 3, 'turn_color': 'white', 'selected': False, 'x_pos': 322, 'y_pos': 200}, {'colNum': 4, 'turn_color': 'white', 'selected': False, 'x_pos': 377, 'y_pos': 200}, {'colNum': 5, 'turn_color': 'white', 'selected': False, 'x_pos': 432, 'y_pos': 200}, {'colNum': 6, 'turn_color': None, 'selected': False, 'x_pos': 487, 'y_pos': 200}, {'colNum': 7, 'turn_color': None, 'selected': False, 'x_pos': 542, 'y_pos': 200}], 'row4': [{'colNum': 0, 'turn_color': None, 'selected': False, 'x_pos': 130, 'y_pos': 247}, {'colNum': 1, 'turn_color': None, 'selected': False, 'x_pos': 185, 'y_pos': 247}, {'colNum': 2, 'turn_color': None, 'selected': False, 'x_pos': 240, 'y_pos': 247}, {'colNum': 3, 'turn_color': None, 'selected': False, 'x_pos': 295, 'y_pos': 247}, {'colNum': 4, 'turn_color': None, 'selected': False, 'x_pos': 350, 'y_pos': 247}, {'colNum': 5, 'turn_color': 'black', 'selected': False, 'x_pos': 405, 'y_pos': 247}, {'colNum': 6, 'turn_color': 'black', 'selected': False, 'x_pos': 460, 'y_pos': 247}, {'colNum': 7, 'turn_color': None, 'selected': False, 'x_pos': 515, 'y_pos': 247}, {'colNum': 8, 'turn_color': None, 'selected': False, 'x_pos': 570, 'y_pos': 247}], 'row5': [{'colNum': 0, 'turn_color': None, 'selected': False, 'x_pos': 157, 'y_pos': 295}, {'colNum': 1, 'turn_color': 'black', 'selected': False, 'x_pos': 212, 'y_pos': 295}, {'colNum': 2, 'turn_color': None, 'selected': False, 'x_pos': 267, 'y_pos': 295}, {'colNum': 3, 'turn_color': None, 'selected': False, 'x_pos': 322, 'y_pos': 295}, {'colNum': 4, 'turn_color': 'white', 'selected': False, 'x_pos': 377, 'y_pos': 295}, {'colNum': 5, 'turn_color': None, 'selected': False, 'x_pos': 432, 'y_pos': 295}, {'colNum': 6, 'turn_color': 'black', 'selected': False, 'x_pos': 487, 'y_pos': 295}, {'colNum': 7, 'turn_color': None, 'selected': False, 'x_pos': 542, 'y_pos': 295}], 'row6': [{'colNum': 0, 'turn_color': None, 'selected': False, 'x_pos': 185, 'y_pos': 343}, {'colNum': 1, 'turn_color': 'black', 'selected': False, 'x_pos': 240, 'y_pos': 343}, {'colNum': 2, 'turn_color': 'white', 'selected': False, 'x_pos': 295, 'y_pos': 343}, {'colNum': 3, 'turn_color': 'black', 'selected': False, 'x_pos': 350, 'y_pos': 343}, {'colNum': 4, 'turn_color': 'black', 'selected': False, 'x_pos': 405, 'y_pos': 343}, {'colNum': 5, 'turn_color': None, 'selected': False, 'x_pos': 460, 'y_pos': 343}, {'colNum': 6, 'turn_color': None, 'selected': False, 'x_pos': 515, 'y_pos': 343}], 'row7': [{'colNum': 0, 'turn_color': 'black', 'selected': False, 'x_pos': 212, 'y_pos': 390}, {'colNum': 1, 'turn_color': 'black', 'selected': False, 'x_pos': 267, 'y_pos': 390}, {'colNum': 2, 'turn_color': 'black', 'selected': False, 'x_pos': 322, 'y_pos': 390}, {'colNum': 3, 'turn_color': None, 'selected': False, 'x_pos': 377, 'y_pos': 390}, {'colNum': 4, 'turn_color': None, 'selected': False, 'x_pos': 432, 'y_pos': 390}, {'colNum': 5, 'turn_color': None, 'selected': False, 'x_pos': 487, 'y_pos': 390}], 'row8': [{'colNum': 0, 'turn_color': None, 'selected': False, 'x_pos': 240, 'y_pos': 438}, {'colNum': 1, 'turn_color': None, 'selected': False, 'x_pos': 295, 'y_pos': 438}, {'colNum': 2, 'turn_color': 'black', 'selected': False, 'x_pos': 350, 'y_pos': 438}, {'colNum': 3, 'turn_color': 'black', 'selected': False, 'x_pos': 405, 'y_pos': 438}, {'colNum': 4, 'turn_color': 'black', 'selected': False, 'x_pos': 460, 'y_pos': 438}]}, 'white', 2)
