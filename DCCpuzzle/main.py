import sys
from puzzle import Puzzle15
from algorithms import BFS, DFS, AStar
from focal_search import FocalSearch
from heuristics import get_heuristic
from display import print_summary, print_path


def main():
    if len(sys.argv) < 5:
        print("Uso: python main.py <dificultad_problema> <número_problema> <heurística_inadmisible> <heurística_admisible> [--show]")
        sys.exit(1)

    # 1) Leer args
    dif_prob      = sys.argv[1]
    prob_idx      = sys.argv[2]
    inad_h_name   = sys.argv[3]
    adm_h_name    = sys.argv[4]
    show_path     = "--show" in sys.argv

    # 2) Construir nombre de fichero
    problem_file = f"{dif_prob}/prob_{prob_idx}.txt"

    # 3) Obtener funciones heurísticas
    inad_h = get_heuristic(inad_h_name)
    adm_h  = get_heuristic(adm_h_name)

    # 4) Cargar problema
    p    = Puzzle15(problem_file)
    init = p.initial_state

    # 5) Instanciar algoritmos
    algorithms = [
        #("DFS", DFS(p)), # Parte 1 
        #("BFS", BFS(p)), # Parte 1 
        #(f"A* ({adm_h_name})", AStar(p, adm_h)), # Parte 2 y Parte 3
        ("Focal w=1", FocalSearch(init, inad_h, adm_h, weight=1)),         # Parte 3
        (f"Focal w=1.2", FocalSearch(init, inad_h, adm_h, weight=1.2)),    # Parte 3
        (f"Focal w=1.5", FocalSearch(init, inad_h, adm_h, weight=1.5)),    # Parte 3
        (f"Focal w=2", FocalSearch(init, inad_h, adm_h, weight=2))         # Parte 3
    ]

    # 6) Ejecutar y recoger resultados
    results = []
    print('\n'*4)
    for name, alg in algorithms:
        print(f"Estamos corriendo {name} ...\n", end='', flush=True)
        if isinstance(alg, FocalSearch):
            res = alg.solve()
        else:
            res = alg.solve()
        results.append((name, res))

    print()
    # 7) Mostrar tabla comparativa
    print_summary(results)

    # 8) (Opcional) si piden --show, mostrar el camino de la última ejecución
    if show_path and results:
        last_name, last_res = results[-1]
        if last_res.path:
            print(f"\nCamino solución para «{last_name}»:")
            print_path(last_res.path[-1])

if __name__ == "__main__":
    main()