import argparse

# Globale Variable für den ausgewählten Algorithmus
selected_algorithm = None


def parse_args():
    global selected_algorithm

    parser = argparse.ArgumentParser(description="Labyrinth-Explorer")
    parser.add_argument("algorithm", type=int, choices=[1, 2, 3, 4, 5, 6, 7, 8])
    args = parser.parse_args()
    return args.algorithm

    # Setzen der globalen Variable basierend auf dem Argument



def get_algorithm_choice():
    if isinstance(parse_args(), int):
        return parse_args()
    else:
        raise ValueError("Unbekannter Algorithmus. Bitte wählen Sie 'astar' oder 'dijkstra'.")
