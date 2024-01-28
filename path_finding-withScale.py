"""
I will test the following algorithms:
1. A*
2. Dijkstra URL: https://www.youtube.com/watch?v=KiOso3VE-vI
3. BFS URL: https://www.youtube.com/watch?v=sV-nNFEfo_s
4. Maze generation URL: https://youtu.be/sVcB8vUFlmU
5. DFS URL: https://www.youtube.com/watch?v=Sbciimd09h4
6. Bidirectional search URL: https://www.youtube.com/watch?v=SABX6YggDTU
7. Bellman-Ford URL: https://www.youtube.com/watch?v=obWXjtg0L64
8. Floyd-Warshall URL: https://www.youtube.com/watch?v=5xKGW8cflDA
"""
from datetime import datetime
import pygame  # for visualization
import queue  # for A* algorithm, the queue library is used to store the nodes in the priority queue
import numpy as np  # for maze generation
import random  # for maze generation
import traceback
import sys
from functools import lru_cache
from argument_parser import get_algorithm_choice # for console arguments

try:
    # Initialisierung von Pygame
    pygame.init()

    # Bildschirmgröße und Labyrinthgröße
    screen_size = (1920, 1080)
    width, height = (1920, 1080)

    # Pygame-Fenster einrichten
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Labyrinth Generator")

    # Farbdefinitionen
    ORANGE = (255, 165, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    LIGHT_BLUE = (45, 45, 255)

    wall_freq = 0.0003  # Wahrscheinlichkeit für eine Wand an einer bestimmten Position
    buffer = 20

    start_x, start_y = 0, 0
    end_x, end_y = 0, 0

    # Labyrinth als 2D-Array initialisieren
    labyrinth = np.zeros((height, width))

    # Skaliertes Labyrinth als 2D-Array initialisieren
    scaled_labyrinth = None


    # Funktion zum Markieren der Pufferzone im Labyrinth
    def mark_buffer_zone(labyrinth, buffer):
        # Markiert die Ränder des Labyrinths als Gefahrenzone, um die Platzierung von Elementen zu verhindern
        labyrinth[:buffer, :] = 9
        labyrinth[-buffer:, :] = 9
        labyrinth[:, :buffer] = 9
        labyrinth[:, -buffer:] = 9


    # Funktion zum Finden zufälliger Positionen für Start- und Endpunkte
    def find_random_positions(labyrinth, width, height, buffer):
        positions = []
        bad_indices_x = set()
        bad_indices_y = set()

        while len(positions) < 1:  # Da wir nur eine Position für Start und Ende benötigen
            x = random.randint(buffer, width - buffer - 10)  # -10, um Platz für 9x9-Bereich zu lassen
            y = random.randint(buffer, height - buffer - 10)

            # Wenn die Anzahl der schlechten Indizes zu hoch wird, wählen Sie einfach eine Position
            if len(bad_indices_x) > 2000:
                if x not in bad_indices_x:
                    positions.append((x, y))
                    break
            if len(bad_indices_y) > 2000:
                if y not in bad_indices_y:
                    positions.append((x, y))
                    break

            if x not in bad_indices_x and y not in bad_indices_y:
                # Überprüfen, ob ein 9x9 Bereich um (x, y) frei ist
                if np.all(labyrinth[y:y + 9, x:x + 9] == 0):
                    positions.append((x, y))
                else:
                    bad_indices_x.add(x)
                    bad_indices_y.add(y)

        return positions


    def place_walls(labyrinth, buffer, wall_freq):
        """ Places walls in the labyrinth at random positions with fixed size. """
        rows, cols = labyrinth.shape

        for y in range(buffer, rows - buffer - 17):  # Reserve space for the maximum wall size
            for x in range(buffer, cols - buffer - 17):
                # Randomly decides whether to place a wall at this position
                if random.random() < wall_freq:
                    # Randomly chooses if the wall is horizontal or vertical
                    if random.choice([True, False]):  # Horizontal
                        wall_width = 28
                        wall_height = 12
                        if x + wall_width < cols - buffer and np.all(labyrinth[y:y + wall_height, x:x + wall_width] == 0):
                            # Check if there is enough space for the wall and the path
                            if np.all(labyrinth[y + wall_height:y + wall_height + 10, x:x + wall_width] == 0):
                                labyrinth[y:y + wall_height, x:x + wall_width] = 1
                    else:  # Vertical
                        wall_width = 12
                        wall_height = 17
                        if y + wall_height < rows - buffer and np.all(labyrinth[y:y + wall_height, x:x + wall_width] == 0):
                            # Check if there is enough space for the wall and the path
                            if np.all(labyrinth[y + wall_height:y + wall_height + 10, x:x + wall_width] == 0):
                                labyrinth[y:y + wall_height, x:x + wall_width] = 1


    def place_start_and_end(labyrinth, start_positions, end_positions):
        """ Platziert Start- und Endpunkte im Labyrinth. """
        global start_x, start_y, end_x, end_y
        if start_positions:
            start_x, start_y = start_positions[0]
            labyrinth[start_y:start_y + 9, start_x:start_x + 9] = 2

        if end_positions:
            end_x, end_y = end_positions[0]
            labyrinth[end_y:end_y + 9, end_x:end_x + 9] = 3


    # Pufferzone und Wände im Labyrinth markieren
    mark_buffer_zone(labyrinth, buffer)
    place_walls(labyrinth, buffer, wall_freq)

    # Zufällige Positionen für Start- und Endpunkt finden und platzieren
    start_positions = find_random_positions(labyrinth, width, height, buffer)
    end_positions = find_random_positions(labyrinth, width, height, buffer)
    place_start_and_end(labyrinth, start_positions, end_positions)


    def scale_labyrinth(surface):
        # Erstellen eines leeren Labyrinths mit den Abmessungen der Oberfläche
        new_width, new_height = surface.get_width(), surface.get_height()
        scaled_labyrinth = np.zeros((new_height, new_width))

        # Zählvariablen für das erste Vorkommen von Start- und Endpunkt
        i_start, i_end = 0, 0

        for y in range(new_height):
            for x in range(new_width):
                color = surface.get_at((x, y))

                if color == WHITE:
                    scaled_labyrinth[y, x] = 1  # Wand
                elif color == GREEN:
                    scaled_labyrinth[y, x] = 2  # Startpunkt
                    i_start += 1
                    if i_start == 1:  # Setzen Sie die Startposition nur beim ersten Vorkommen
                        start_x, start_y = x, y
                elif color == RED:
                    scaled_labyrinth[y, x] = 3  # Endpunkt
                    i_end += 1
                    if i_end == 1:  # Setzen Sie die Endposition nur beim ersten Vorkommen
                        end_x, end_y = x, y
                elif color == LIGHT_BLUE:
                    scaled_labyrinth[y, x] = 9  # Pufferzone

        return scaled_labyrinth


    # Funktion zum Finden der Position des orangenen Pixels
    def find_orange_pixel(surface):
        width, height = surface.get_size()  # Abfrage der Größe des Surface-Objekts
        for y in range(height):
            for x in range(width):
                color = surface.get_at((x, y))
                if color == ORANGE:
                    return x, y

        for y in range(height):
            for x in range(width):
                color = surface.get_at((x, y))
                if color == ORANGE:
                    return x, y


    # Funktion zum Finden der Position des blauen Pixels
    def find_end_position(surface):
        width, height = surface.get_size()  # Abfrage der Größe des Surface-Objekts
        for y in range(height):
            for x in range(width):
                color = surface.get_at((x, y))
                if color == RED:
                    return x+6, y+6



    class Labyrinth:
        def __init__(self, labyrinth):
            self.labyrinth = labyrinth
            self.surface = pygame.Surface(screen_size)
            self.draw_labyrinth()

        def draw_labyrinth(self):
            rows, cols = self.labyrinth.shape

            for y in range(rows):
                for x in range(cols):
                    if self.labyrinth[y, x] == 1:  # Wand
                        pygame.draw.rect(self.surface, WHITE, (x, y, 1, 1))
                    elif self.labyrinth[y, x] == 2:  # Startpunkt
                        pygame.draw.rect(self.surface, GREEN, (x, y, 9, 9))
                        # Setze das mittlere Pixel auf Orange
                        pygame.draw.rect(self.surface, ORANGE, (x + 4, y + 4, 2, 2))
                    elif self.labyrinth[y, x] == 3:  # Endpunkt
                        pygame.draw.rect(self.surface, RED, (x, y, 9, 9))
                    elif self.labyrinth[y, x] == 9:  # Pufferzone
                        pygame.draw.rect(self.surface, LIGHT_BLUE, (x, y, 1, 1))

            # Skaliert die Surface auf 60% ihrer ursprünglichen Größe
            self.scale_surface()

        def scale_surface(self):
            # Berechnet die neue Größe als 60% der ursprünglichen Größe
            original_width, original_height = self.surface.get_size()
            new_width = int(original_width * 0.85)
            new_height = int(original_height * 0.80)
            self.surface = pygame.transform.scale(self.surface, (new_width, new_height))
            global scaled_labyrinth
            # Skalieren Sie das Labyrinth nach dem Zeichnen auf die Oberfläche
            scaled_labyrinth = scale_labyrinth(self.surface)

        def blit(self):
            # Blitzen der skalierten Surface auf den Bildschirm
            screen.blit(self.surface, (0, 0))


    # Labyrinth-Instanz erstellen
    labyrinth_instance = Labyrinth(labyrinth)


    class Explorer:
        def __init__(self, start, start2, end, end2, color):
            self.surface = None
            self.start_position = (start, start2)
            self.end_position = (end, end2)
            self.color = color  # Farbe des Explorers
            self.labyrinth = None  # Das Labyrinth, das skaliert wurde
            self.algorithm_choice = None  # Die Wahl des Algorithmus

            self.open_set = queue.PriorityQueue()  # Tracks cells to be explored
            self.open_set.put(
                (0, self.heuristic(self.start_position), self.start_position))  # Add the start position to the queue
            self.came_from = {}  # Tracks the path
            self.g_cost = {self.start_position: 0}  # Tracks the G cost of each cell
            self.f_cost = {self.start_position: self.heuristic(self.start_position)}  # Tracks the F cost of each cell
            self.current_position = self.start_position  # Tracks the current position of the explorer
            self.path_found = False  # Flag to indicate if the path has been found
            self.steps = 0  # Tracks the number of steps taken

            # Logfile erstellen
            self.logfile = open("logfile.txt", "w")

        def spread(self):
            match self.algorithm_choice:
                case 1:
                    # Implement A* algorithm logic here
                    next_position = self.a_star_step()
                    if next_position is not None:
                        self.current_position = next_position
                        self.draw()

                    self.steps += 1
                    if self.steps % 10 == 0:
                        self.log_step()
                case 2:
                    # Dijkstra's Algorithmus Logik
                    next_position = self.dijkstra_step()
                    if next_position is not None:
                        self.current_position = next_position
                        self.draw()

                    self.steps += 1
                    if self.steps % 10 == 0:
                        self.log_step()
                case 3:
                    # Implement BFS algorithm logic here
                    pass
                case 4:
                    # Maze generation logic (might not be applicable for spreading)
                    pass
                case 5:
                    # Implement DFS algorithm logic here
                    pass
                case 6:
                    # Implement Bidirectional search algorithm logic here
                    pass
                case 7:
                    # Implement Bellman-Ford algorithm logic here
                    pass
                case 8:
                    # Implement Floyd-Warshall algorithm logic here
                    pass
                case _:
                    # Default case if an unknown choice is provided
                    print("Unknown algorithm choice")

        def a_star_step(self):
            # Überprüfen, ob der Pfad noch nicht gefunden wurde und ob es noch Knoten gibt, die erkundet werden müssen
            if not self.path_found and not self.open_set.empty():
                # Entfernen Sie den Knoten mit den niedrigsten F-Kosten aus der Warteschlange
                current = self.open_set.get()[2]

                # Überprüfen, ob der aktuelle Knoten der Zielknoten ist
                if current == self.end_position:
                    self.path_found = True  # Setzen Sie die Flagge, dass der Pfad gefunden wurde
                    self.logfile.close()  # Schließen Sie die Logdatei
                    # Rufen Sie die Methode auf, um den gefundenen Pfad zurückzuverfolgen und zurückzugeben
                    return self.reconstruct_path(self.came_from, current)

                # Überprüfen Sie jeden Nachbarn des aktuellen Knotens
                for neighbor in self.get_neighbors(current):
                    # Berechnen Sie die G-Kosten für den Nachbarn (aktueller G-Wert + 1)
                    temp_g_score = self.g_cost[current] + 1

                    # Wenn dieser Weg zum Nachbarn besser ist als ein zuvor gefundener Weg, speichern Sie ihn
                    if temp_g_score < self.g_cost.get(neighbor, float('inf')):
                        # Aktualisieren Sie den Elternknoten und die Kosten des Nachbarn
                        self.came_from[neighbor] = current
                        self.g_cost[neighbor] = temp_g_score

                        # Die kosten für Wände umgehen
                        wall_penalty = 10000
                        self.f_cost[neighbor] = temp_g_score + self.heuristic(neighbor) + (self.labyrinth[neighbor[1]][neighbor[0]] == 1) * wall_penalty
                        # Fügen Sie den Nachbarn mit den berechneten F-Kosten zur Warteschlange hinzu
                        self.open_set.put((self.f_cost[neighbor], self.heuristic(neighbor), neighbor))

                # Geben Sie die aktuelle Position zurück
                return current

            # Wenn kein weiterer Schritt möglich ist oder der Pfad bereits gefunden wurde, geben Sie None zurück
            return None

        def dijkstra_step(self):
            if not self.path_found and not self.open_set.empty():
                current = self.open_set.get()[2]
                if current == self.end_position:
                    self.path_found = True
                    self.logfile.close()
                    return self.reconstruct_path(self.came_from, current)

                for neighbor in self.get_neighbors(current):
                    temp_g_score = self.g_cost[current] + 1  # Die Kosten für einen Schritt sind immer 1

                    if temp_g_score < self.g_cost.get(neighbor, float('inf')):
                        self.came_from[neighbor] = current
                        self.g_cost[neighbor] = temp_g_score

                        wall_penalty = 10000
                        total_cost = temp_g_score + (self.labyrinth[neighbor[1]][neighbor[0]] == 1) * wall_penalty
                        self.open_set.put((total_cost, total_cost, neighbor))

                return current
            return None

        @lru_cache(maxsize=None)
        def heuristic(self, position):
            # Heuristikfunktion: Berechnet die Manhattan-Distanz vom aktuellen Knoten zum Endknoten.
            x1, y1 = position
            x2, y2 = self.end_position
            return abs(x1 - x2) + abs(y1 - y2)

        @lru_cache(maxsize=None)
        def get_neighbors(self, position):
            # Gibt die gültigen Nachbarn eines Knotens zurück, wobei Wände und die Pufferzone ausgeschlossen werden.
            neighbors = []
            x, y = position
            directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Oben, Rechts, Unten, Links

            # Überprüfen Sie jede mögliche Bewegungsrichtung (links, rechts, oben, unten) und fügen Sie gültige Nachbarn hinzu.
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                # Überprüft, ob die Position innerhalb des Labyrinths liegt
                if 0 <= nx < self.labyrinth.shape[1] and 0 <= ny < self.labyrinth.shape[0]:
                    # Überprüft, ob die Position keine Wand, keine Pufferzone ist und nicht bereits besucht wurde
                    if np.all([self.labyrinth[ny][nx] != 1, self.labyrinth[ny][nx] != 9, (nx, ny) not in self.came_from]):
                        neighbors.append((nx, ny))

            return neighbors

        def reconstruct_path(self, came_from, current):
            # Rekonstruiert den Pfad rückwärts vom Endpunkt zum Startpunkt.
            total_path = [current]
            # Verfolgen Sie den Pfad rückwärts anhand der Elternknoten, die in `came_from` gespeichert sind.
            while current in came_from:
                current = came_from[current]
                total_path.insert(0, current)
            return total_path

        def draw(self):
            # Visualisieren Sie die aktuelle Position des Explorers
            if len(self.current_position) == 2:
                x, y = self.current_position
                # Zeichnen eines orangen Rechtecks an der aktuellen Position
                pygame.draw.rect(self.surface, self.color, (x, y, 1, 1))

        def log_step(self):
            try:
                last_position = self.came_from.get(tuple(self.current_position), "Start")
                log_message = f"Step {self.steps}: From {last_position} to {self.current_position}\n"
                self.logfile.write(log_message)
            except Exception as e:
                print(f"Error: {str(e)}")


    orange_x, orange_y = find_orange_pixel(labyrinth_instance.surface)
    end_x, end_y = find_end_position(labyrinth_instance.surface)

    # Explorer-Instanz erstellen - Explorer ist der Algorithmus, der sich durch das Labyrinth bewegt:
    # Überprüfen, ob die Pixel gefunden wurden und Explorer-Instanz entsprechend erstellen
    if orange_x is not None and orange_y is not None:
        explorer = Explorer(orange_x, orange_y, end_x, end_y, ORANGE)
    else:
        # Falls die Pixel nicht gefunden wurden, Standardstart- und Endpunkte verwenden
        explorer = Explorer(start_x, start_y, end_x, end_y, ORANGE)

    explorer.surface = labyrinth_instance.surface
    explorer.labyrinth = scaled_labyrinth
    explorer.algorithm_choice = get_algorithm_choice()

    # Clock-Objekt für die Framerate-Kontrolle
    clock = pygame.time.Clock()

    # Haupt-Event-Schleife
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        labyrinth_instance.blit()

        if not explorer.path_found:
            explorer.spread()
        explorer.draw()

        # update the screen
        pygame.display.flip()

        clock.tick(60)  # Setzt die Framerate auf 60 FPS

    pygame.quit()
except pygame.error as e_:
    traceback.print_exc()  # Gibt den kompletten Traceback aus

    try:
        with open("ErrorFile.txt", "a") as error_file:
            error_file.write(f"\n\n\n")
            # Datum und Uhrzeit zum Fehlerprotokoll hinzufügen
            error_file.write(f"Date and time: {str(datetime.now())}\n")
            traceback.print_exc(file=error_file)  # Schreibt den Traceback in die Datei
            error_file.close()
    except Exception as e:
        print("Warning: Could not write to ErrorFile.txt. High probability that the "
              "program haven't got the permission to write to the files.")
except Exception as e:
    traceback.print_exc()  # Gibt den kompletten Traceback aus
    try:
        with open("ErrorFile.txt", "a") as error_file:
            error_file.write(f"\n\n")
            # Datum und Uhrzeit zum Fehlerprotokoll hinzufügen
            error_file.write(f"Date and time: {str(datetime.now())}")
            traceback.print_exc(file=error_file)
            error_file.close()
    except Exception as e:
        print("Warning: Could not write to ErrorFile.txt. High probability that the "
              "program haven't got the permission to write to the files.")
finally:
    pygame.quit()
