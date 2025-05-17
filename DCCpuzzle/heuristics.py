import numpy as np
import tensorflow as tf
import os
from litemodel import LiteModel, from_file, from_keras_model

# NO MODIFICAR
_model_nn = None
_model_input_idx = None
_model_output_idx = None
_model_input_dtype = None

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def get_heuristic(heuristic):
    if heuristic == "manhattan":
        return manhattan
    elif heuristic == "euclidian":
        return euclidian
    elif heuristic == "nn":
        _load_nn_model()
        return nn_policy
    elif heuristic ==  "manhattan_linear":
        return manhattan_linear
    elif heuristic == "zero":
        return lambda s: 0
    elif heuristic == "inadmisible_pesada":  
        return inadmisible_pesada
    else:
        raise ValueError(f"Heurística desconocida: {heuristic}")

def _load_nn_model():
    # NO MODIFICAR
    global _model_nn, _model_input_idx, _model_output_idx, _model_input_dtype
    if _model_nn is None:
        _model_nn = from_keras_model("15puzzle_solver_model.h5")
        interp = _model_nn.interpreter
        inp_det = interp.get_input_details()[0]
        out_det = interp.get_output_details()[0]
        _model_input_idx  = inp_det["index"]
        _model_input_dtype= inp_det["dtype"]
        _model_output_idx = out_det["index"]
    
def nn_policy(state):
    # NO MODIFICAR
    one_hot_bits = []
    for row in state.board:
        for val in row:
            n = 0 if val == "X" else int(val)
            vec = [0]*16
            vec[n] = 1
            one_hot_bits.extend(vec)

    arr = np.array([one_hot_bits], dtype=_model_input_dtype)

    interp = _model_nn.interpreter
    interp.set_tensor(_model_input_idx, arr)
    interp.invoke()
    out = interp.get_tensor(_model_output_idx)[0]
    # asume que out.sum()==1
    return out

def manhattan(state):
    objetivo = {
        "1": (0, 0), "2": (0, 1), "3": (0, 2), "4": (0, 3),
        "5": (1, 0), "6": (1, 1), "7": (1, 2), "8": (1, 3),
        "9": (2, 0), "10": (2, 1), "11": (2, 2), "12": (2, 3),
        "13": (3, 0), "14": (3, 1), "15": (3, 2),
        "X": (3, 3) 
    }
    dist = 0
    for i in range(4):
        for j in range(4):
            val = state.board[i][j]
            gx, gy = objetivo[val]
            dist += abs(i - gx) + abs(j - gy)
    return dist

def euclidian(state):
    objetivo = {
        "1": (0, 0), "2": (0, 1), "3": (0, 2), "4": (0, 3),
        "5": (1, 0), "6": (1, 1), "7": (1, 2), "8": (1, 3),
        "9": (2, 0), "10": (2, 1), "11": (2, 2), "12": (2, 3),
        "13": (3, 0), "14": (3, 1), "15": (3, 2),
        "X": (3, 3)
    }
    dist = 0
    for i in range(4):
        for j in range(4):
            val = state.board[i][j]
            gx, gy = objetivo[val]
            dist += ((i - gx) ** 2 + (j - gy) ** 2) ** 0.5
    return dist

def manhattan_linear(state):
    objetivo = {
        "1": (0, 0), "2": (0, 1), "3": (0, 2), "4": (0, 3),
        "5": (1, 0), "6": (1, 1), "7": (1, 2), "8": (1, 3),
        "9": (2, 0), "10": (2, 1), "11": (2, 2), "12": (2, 3),
        "13": (3, 0), "14": (3, 1), "15": (3, 2),
        "X": (3, 3)
    }

    dist = 0
    linear_conflict = 0

    for i in range(4):
        row_vals = []
        col_vals = []
        for j in range(4):
            val_row = state.board[i][j]
            gx_row, gy_row = objetivo[val_row]
            dist += abs(i - gx_row) + abs(j - gy_row)
            if gx_row == i and val_row != "X":
                row_vals.append((j, gy_row))

            val_col = state.board[j][i]
            gx_col, gy_col = objetivo[val_col]
            if gy_col == i and val_col != "X":
                col_vals.append((j, gx_col))

        for a in range(len(row_vals)):
            for b in range(a + 1, len(row_vals)):
                if row_vals[a][1] > row_vals[b][1]:
                    linear_conflict += 1

        for a in range(len(col_vals)):
            for b in range(a + 1, len(col_vals)):
                if col_vals[a][1] > col_vals[b][1]:
                    linear_conflict += 1

    return dist + 2 * linear_conflict

def inadmisible_pesada(state):
    """
    Heurística no admisible personalizada:
    Suma la distancia de Manhattan con una penalización cuadrática
    en función del número de piezas mal ubicadas.
    """
    manhattan_value = manhattan(state)
    
    # Convierte el tablero 2D en una lista plana de números esperados
    objetivo = ['1', '2', '3', '4', '5', '6', '7', '8',
                '9', '10', '11', '12', '13', '14', '15', 'X']
    current = [val for row in state.board for val in row]
    
    misplaced = sum(1 for i in range(16) if current[i] != objetivo[i] and current[i] != 'X')
    penalizacion = (misplaced ** 2) * 0.1
    return manhattan_value + penalizacion

