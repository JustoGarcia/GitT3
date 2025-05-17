from board.board_helper import BoardHelper

players = [1, 2]

def minimax(board_array, player_id, fixed_player_id, depth, max_player, use_alphabeta, eval_function, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or BoardHelper.is_terminal_state(board_array, players):
        return eval_function(board_array, fixed_player_id), None

    best_score = float('-inf') if max_player else float('inf')
    best_move = None

    for move, possible_board in BoardHelper.get_possible_next_states(board_array, player_id):
        opponent_id = 3 - player_id
        score, _ = minimax(possible_board, opponent_id, fixed_player_id, depth - 1, not max_player, use_alphabeta, eval_function, alpha, beta)

        if max_player:
            if score > best_score:
                best_score = score
                best_move = move

            if use_alphabeta:
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Poda beta

        else:
            if score < best_score:
                best_score = score
                best_move = move

            if use_alphabeta:
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Poda alfa

    return best_score, best_move
