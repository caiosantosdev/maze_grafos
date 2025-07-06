import sys
import json
import os
from matplotlib import pyplot as plt
from a_star import astar
from dijkstra import dijkstra_custom
from matriz_utils import build_graph, gerar_matriz_labirinto, salvar_matriz_como_json
class MazeVisualizer:
    def __init__(self, reuse_maze=False, existing_maze=None):
        self.jaCarregouMaze = False
        self.rows = 30
        self.cols = 30
        self.maze = existing_maze if reuse_maze and existing_maze else gerar_matriz_labirinto(self.rows, self.cols, 0.2)
        self.graph = build_graph(self.maze)
        self.reset_estado()
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.menu_algoritmo()

    def reset_estado(self):
        self.start = None
        self.end = None
        self.path = None
        self.visited = None
        

    def menu_algoritmo(self):
        if not self.jaCarregouMaze:
            self.jaCarregouMaze = True
            opcao_labirinto = input("Deseja gerar um novo labirinto? (s/n): ").strip().lower()
            if opcao_labirinto == 's':
                try:
                    self.rows = int(input("Digite o número de linhas: ").strip())
                    self.cols = int(input("Digite o número de colunas: ").strip())
                    densidade = float(input("Digite a densidade de obstáculos (0 a 1): ").strip())
                    if not (0 <= densidade <= 1):
                        raise ValueError
                except ValueError:
                    print("Entrada inválida. Usando valores padrão: 30x30 e densidade 0.2")
                    self.rows, self.cols, densidade = 30, 30, 0.2

                self.maze = gerar_matriz_labirinto(self.rows, self.cols, densidade)
                salvar = input("Deseja salvar este labirinto? (s/n): ").strip().lower()
                if salvar == 's':
                    salvar_matriz_como_json(self.maze)
                self.graph = build_graph(self.maze)

            else:
                nome_labirinto = input("Digite o nome do labirinto (sem .json): ").strip().lower()
                caminho_arquivo = f"labirintos/{nome_labirinto}.json"
                if os.path.exists(caminho_arquivo):
                    with open(caminho_arquivo, 'r') as f:
                        self.maze = json.load(f)
                        self.rows = len(self.maze)
                        self.cols = len(self.maze[0])
                        self.graph = build_graph(self.maze)
                        print("Labirinto carregado com sucesso.")
                        
                else:
                    print("Arquivo não encontrado. Gerando novo labirinto padrão.")
                    self.rows, self.cols = 30, 30
                    self.maze = gerar_matriz_labirinto(self.rows, self.cols, 0.2)
                    self.graph = build_graph(self.maze)
                

        self.reset_estado()
        opcoes = {"1": "Dijkstra", "2": "A*"}
        while True:
            escolha = input("Digite 1 para Dijkstra ou 2 para A*: (Digite R para reiniciar labirinto ou Q para sair)> ").strip()
            if escolha.upper() == 'R':
                self.__init__()  # Gera novo labirinto
                self.draw_maze()
                plt.title("Clique para escolher o ponto de INÍCIO e depois o FIM")
                plt.show()
                return
            elif escolha.upper() == 'Q':
                print("Encerrando o programa.")
                sys.exit()
            elif escolha in opcoes:
                self.algoritmo = opcoes[escolha]
                self.reset_estado()
                self.draw_maze()
                plt.title("Clique para escolher o ponto de INÍCIO e depois o FIM")
                plt.show()
                break

    def draw_maze(self):
        self.ax.clear()
        for r in range(self.rows):
            for c in range(self.cols):
                pos = (r, c)
                if self.maze[r][c] == 1:
                    color = 'black'
                elif pos == self.start:
                    color = 'green'
                elif pos == self.end:
                    color = 'red'
                elif self.path and pos in self.path:
                    color = 'blue'
                elif self.visited and pos in self.visited:
                    color = '#add8e6'
                else:
                    color = 'white'
                rect = plt.Rectangle([c, self.rows - r - 1], 1, 1, facecolor=color, edgecolor='gray')
                self.ax.add_patch(rect)
        self.ax.set_xlim(0, self.cols)
        self.ax.set_ylim(0, self.rows)
        self.ax.set_aspect('equal')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        def custom_format_coord(x, y):
            col = int(x)
            row = self.rows - int(y) - 1
            return f"linha={row}, coluna={col}"

        self.ax.format_coord = custom_format_coord

        self.fig.canvas.draw()
    def onclick(self, event):
        if event.inaxes != self.ax:
            return
        col = int(event.xdata)
        row = self.rows - int(event.ydata) - 1
        if self.maze[row][col] == 1:
            print("Célula bloqueada. Escolha uma célula livre.")
            return

        pos = (row, col)
        if not self.start:
            self.start = pos
            print(f"Início definido em {pos}")
        elif not self.end:
            self.end = pos
            print(f"Fim definido em {pos}")
            self.executar_algoritmo()
        self.draw_maze()

    def executar_algoritmo(self):
        if self.algoritmo == "Dijkstra":
            self.path, elapsed, self.visited = dijkstra_custom(self.graph, self.start, self.end)
        else:
            self.path, elapsed, self.visited = astar(self.graph, self.start, self.end)

        if not self.path:
            print("Nenhum caminho encontrado.")
        else:
            print(f"\n--- Resultado com {self.algoritmo} ---")
            print(f"Tamanho do caminho: {len(self.path) - 1}")
            print(f"Nós visitados: {len(self.visited)}")
            print(f"Tempo de execução: {elapsed:.6f}s\n")
        self.draw_maze()
        self.menu_algoritmo()