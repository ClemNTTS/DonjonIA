import random
import matplotlib.pyplot as plt

# Position de l'agent
agent_x = 0
agent_y = 0

tresor_x, tresor_y = 0,0


class UnionFind:
    def __init__(self, n):
        # Initialiser la structure Union-Find avec n éléments
        self.parent = list(range(n))

    def find(self, u):
        # Trouver le représentant de l'ensemble contenant u
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])  # Compression de chemin
        return self.parent[u]

    def union(self, u, v):
        # Unir les ensembles contenant u et v
        pu, pv = self.find(u), self.find(v)
        if pu != pv:
            self.parent[pu] = pv  # Union des ensembles
            return True
        return False

def init_labyrinth(width, height):
    global tresor_x, tresor_y  # Déclarer les variables comme globales
    maze = kruskal_labyrinth(width, height)
    traps = add_traps(maze)
    for trap in traps:
        maze[trap[0]][trap[1]] = 4
    maze, tresor_x, tresor_y = add_tresor(maze, tresor_x, tresor_y)
    maze[0][0] = 3
    return maze, traps, tresor_x, tresor_y

def kruskal_labyrinth(width, height):
    # Créer un labyrinthe initialisé avec des murs (1)
    labyrinth = [[1] * width for _ in range(height)]
    walls = []  # Liste pour stocker les murs à explorer
    uf = UnionFind(width * height)  # Initialiser Union-Find pour gérer les ensembles

    # Parcourir la grille pour définir les cellules et les murs
    for y in range(0, height, 2):
        for x in range(0, width, 2):
            labyrinth[y][x] = 0  # Marquer la cellule comme un chemin (0)
            # Ajouter les murs adjacents à la liste
            if x < width - 2:
                walls.append((x, y, x + 2, y))  # Mur horizontal
            if y < height - 2:
                walls.append((x, y, x, y + 2))  # Mur vertical

    random.shuffle(walls)  # Mélanger les murs pour un ordre aléatoire

    # Parcourir les murs mélangés
    for x1, y1, x2, y2 in walls:
        # Vérifier si les cellules adjacentes peuvent être unies
        if uf.union(y1 * width + x1, y2 * width + x2):
            # Si elles peuvent être unies, abattre le mur entre elles
            labyrinth[(y1 + y2) // 2][(x1 + x2) // 2] = 0

    return labyrinth  # Retourner le labyrinthe généré

def add_traps(labyrinth):
    traps = []
    for y in range(len(labyrinth)):
        for x in range(len(labyrinth[0])):
            if labyrinth[y][x] == 0:
                if random.random() < 0.1:
                    traps.append((y, x))               
    return traps

def add_tresor(labyrinth,tresor_x,tresor_y):
    max_attempts = 100  # Nombre maximum de tentatives pour placer le trésor
    attempts = 0

    while attempts < max_attempts:
        # Trouver une cellule vide (0) dans le labyrinthe
        empty_cells = [(y, x) for y in range(len(labyrinth)) for x in range(len(labyrinth[0])) if labyrinth[y][x] == 0]
        
        if empty_cells:
            # Choisir une cellule vide au hasard
            y, x = random.choice(empty_cells)
            
            # Vérifier les bordures pour s'assurer qu'il y a 3 murs autour
            borders = 0
            if labyrinth[y + 1][x] == 1:
                borders += 1
            if labyrinth[y - 1][x] == 1:
                borders += 1
            if labyrinth[y][x + 1] == 1:
                borders += 1
            if labyrinth[y][x - 1] == 1:
                borders += 1
            
            # Si la cellule a 3 murs, placer le trésor
            if borders == 3 and x != 0 and y != 0:
                labyrinth[y][x] = 2  # Placer le trésor
                tresor_x, tresor_y = x, y
                break  # Sortir de la boucle après avoir placé le trésor
        attempts += 1  # Incrémenter le nombre de tentatives

    return labyrinth,tresor_x,tresor_y

# Afficher le labyrinthe
def display_maze(maze, traps):
    plt.imshow(maze, cmap='gray_r')
    plt.scatter(0, 0, color='red', s=100)
    plt.scatter(tresor_x, tresor_y, color='green', s=100)
    for trap in traps:
        plt.scatter(trap[1], trap[0], color='blue', s=100)
    plt.show(block=False)
    plt.pause(0.5)
    plt.clf()

moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

maze,traps,tresor_x,tresor_y = init_labyrinth(16, 10)
for _ in range(100):
    dx, dy = random.choice(moves)
    new_x, new_y = agent_x + dx, agent_y + dy

    if maze[new_y][new_x] != 1:
        maze[agent_y][agent_x] = 0
        agent_x, agent_y = new_x, new_y
        maze[agent_y][agent_x] = 3
    display_maze(maze,traps)

plt.show()
