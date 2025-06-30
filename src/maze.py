import sys
from matplotlib import pyplot as plt
from a_star import astar
from dijkstra import dijkstra_custom
from matriz_utils import build_graph, gerar_matriz_labirinto, salvar_matriz_como_json


class MazeVisualizer:
    def __init__(self, reuse_maze=False, existing_maze=None):
        print("[INIT] Inicializando MazeVisualizer")
        self.rows = 60
        self.cols = 60
        self.maze = existing_maze 
        if reuse_maze and existing_maze:
            self.maze = existing_maze
        else:
            self.maze = gerar_matriz_labirinto(self.rows, self.cols, 0.2)
            salvar_matriz_como_json(self.maze)
        print("[INIT] Labirinto gerado ou reutilizado")
        self.graph = build_graph(self.maze)
        self.algoritmo = None
        print("[INIT] Grafo construído")
        self.reset_estado()
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.menu_algoritmo()

    def reset_estado(self):
        print("[RESET] Resetando estado...")
        self.start = None
        self.end = None
        self.path = None
        self.visited = None
        # ** Atenção **: não resetar self.algoritmo aqui para não perder o algoritmo selecionado
        print(f"[RESET] Estado após reset: start={self.start}, end={self.end}, path={self.path}, visited={self.visited}, algoritmo={self.algoritmo}")

    def menu_algoritmo(self):
        opcoes = {"1": "Dijkstra", "2": "A*"}
        while True:
            escolha = input("Digite 1 para Dijkstra ou 2 para A*:\n(Digite R para reiniciar labirinto)\n(Digite Q para sair do programa\n)> ").strip()
            if escolha.upper() == 'R':
                print("[MENU] Reiniciando labirinto...")
                self.__init__()  # Gera novo labirinto
                self.draw_maze()
                plt.title("Clique para escolher o ponto de INÍCIO e depois o FIM")
                plt.show()
                return
            elif escolha.upper() == 'Q':
                print("Encerrando o programa.")
                sys.exit()
            elif escolha in opcoes:
                print(f"[MENU] Algoritmo selecionado: {opcoes[escolha]}")
                self.algoritmo = opcoes[escolha]
                self.reset_estado()  # Resetar mas mantendo algoritmo selecionado
                self.draw_maze()
                plt.title("Clique para escolher o ponto de INÍCIO e depois o FIM")
                plt.show()
                break
            else:
                print("[MENU] Opção inválida, tente novamente.")

    def draw_maze(self):
        print("[DRAW] Atualizando visual do labirinto")
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
        self.fig.canvas.draw()

    def onclick(self, event):
        if event.inaxes != self.ax:
            return
        col = int(event.xdata)
        row = self.rows - int(event.ydata) - 1
        if self.maze[row][col] == 1:
            print("[CLICK] Célula bloqueada. Escolha uma célula livre.")
            return

        pos = (row, col)
        if not self.start:
            self.start = pos
            print(f"[CLICK] Início definido em {pos}")
        elif not self.end:
            self.end = pos
            print(f"[CLICK] Fim definido em {pos}")
            print(f"[CLICK] Executando algoritmo {self.algoritmo} com start={self.start} e end={self.end}")
            self.executar_algoritmo()
        self.draw_maze()

    def executar_algoritmo(self):
        if self.algoritmo == "Dijkstra":
            print("[EXEC] Rodando Dijkstra...")
            self.path, elapsed, self.visited = dijkstra_custom(self.graph, self.start, self.end)
        else:
            print("[EXEC] Rodando A*...")
            self.path, elapsed, self.visited = astar(self.graph, self.start, self.end)

        if not self.path:
            print("[EXEC] Nenhum caminho encontrado.")
        else:
            print(f"\n--- Resultado com {self.algoritmo} ---")
            print(f"Tamanho do caminho: {len(self.path) - 1}")
            print(f"Nós visitados: {len(self.visited)}")
            print(f"Tempo de execução: {elapsed:.6f}s\n")
        self.draw_maze()
        self.menu_algoritmo()