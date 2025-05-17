from board.board_helper import BoardHelper
from typing import Tuple, List

def max_n(board_array, player_id, depth, eval_function, player_amount) -> Tuple[List[float], Tuple[int, int]]:
    # Paso base: si llegamos a profundidad 0 o estado terminal
    if depth == 0 or BoardHelper.is_terminal_state(board_array, list(range(1, player_amount + 1))):
        return eval_function(board_array), None

    best_value = [-float('inf')] * player_amount
    best_move = None

    for move, next_board in BoardHelper.get_possible_next_states(board_array, player_id):
        next_player = (player_id % player_amount) + 1  # siguiente jugador en el ciclo 1→2→3→1→...

        child_value, _ = max_n(next_board, next_player, depth - 1, eval_function, player_amount)

        # Solo comparamos el valor del jugador actual
        if child_value[player_id - 1] > best_value[player_id - 1]:
            best_value = child_value
            best_move = move

    return best_value, best_move
