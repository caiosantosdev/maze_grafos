from datetime import datetime
import networkx as nx
import random
import os
import json

def gerar_matriz_labirinto(linhas, colunas, densidade_obstaculos=0.3):
    matriz = []
    for _ in range(linhas):
        linha = []
        for _ in range(colunas):
            if random.random() < densidade_obstaculos:
                linha.append(1)
            else:
                linha.append(0)
        matriz.append(linha)
    return matriz

def salvar_matriz_como_json(matriz):
    # Cria a pasta "labirintos" se não existir
    os.makedirs("labirintos", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"labirintos/labirinto_{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump(matriz, f)

    print(f"[SAVE] Labirinto salvo em '{filename}'")

# --- Construir grafo a partir da matriz ---
def build_graph(maze):
    G = nx.Graph()
    rows = len(maze)
    cols = len(maze[0])
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 0:
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                        G.add_edge((r, c), (nr, nc), weight=1)
    return G