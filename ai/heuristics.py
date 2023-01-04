from board_state.board_query import *


def get_opposite_color(color):
    if color == 'black':
        return 'white'
    else:
        return 'black'


class KatsHeuristic:

    @staticmethod
    def weighted_heuristic(state):
        score_weight = 50
        center_weight = 10
        push_weight = 25
        group_weight = 3

        score = pieces(state[1], state[2]) - pieces(state[1], get_opposite_color(state[2]))
        #print("Score", score)
        center_value = center(state[1], state[2]) - center(state[1], get_opposite_color(state[2]))
        #print("centerValue ", center_value)
        group = len(groups(state[1], state[2])) - len(groups(state[1], get_opposite_color(state[2])))
        #print('group', group)
        push = push_eval(state, center_value)
        #print("Push", push)
        int_value = int(score_weight * score + center_weight * center_value + push_weight * push + group * group_weight)
        return int_value


