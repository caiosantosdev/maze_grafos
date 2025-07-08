# Trabalho de Grafos: Análise comparativa entre Dijkstra e A* utilizando a heurística da distância de Manhattan

## Organização do projeto:
  O projeto foi organizado em dois diretórios, um denominado "labirintos", que armazeno o output da matriz binária utilizada no caso relacionado do algoritmo, e a outra sendo o "src", que contém os código utilizado para a solução do problema.


### labirintos/
  Utilizado para armazenar os labirintos (em formato JSON), que foram utilizados durante as execuções comparativas. 
  O nome dos arquivos tem formato: labirinto_ANOMESDIA_HORAMINUTOSEGUNDO.json

  Labirinto 15x15: labirinto_20250702_232958.json
  
  Labirinto 30x30: labirinto_20250705_195953.json
  
  Labirinto 60x60: labirinto_20250630_122452.json
  

### src/
  Utilizado para armazenar os códigos utilizando na análise comparativa.
 
  #### a_star.py
    Algoritmo A*, que possui como heurística utilizada para as comparações para escolha do melhor caminho como sendo a Distância de Manhattan.
  #### dijkstra.py
    Algoritmo de Dijkstra, que calcula o caminho mínimo entre dois vértices (pontos dentro da matriz) e retorna o caminho, o tempo gasto e os nós visitados.
  #### main.py
    Código de execução principal. Apenas executa o menu do labirinto.
  #### matriz_utilz
    Armazena as funções de leitura de geração de matriz aleatória com obstáculos, escrita de matriz como json e passagem de matriz para estruturas de grafo do networkx
  #### maze.py
    Armazena a classe que gerencia a execução principal do programa. Suas funções se baseiam em: Iniciar os valores do labirinto no contrutor, resetar o estado da matriz ao reiniciar, executar o menu de escolha do algoritmo, desenhar o algoritmo com a biblioteca do matplotlib, salvar o click do mouse para definir os pontos de origem e destino e executar o algoritmo escolhido pelo usuário.


## Bibliotecas utilizadas:

#### sys
  Utilizada para encerrar o programa manualmente com sys.exit() quando o usuário opta por sair no menu. É útil para ter controle sobre a execução do script de forma imediata e segura.

#### matplotlib
  Utilizada para visualização gráfica do labirinto. A biblioteca matplotlib.pyplot permite desenhar a matriz com cores representando paredes, caminhos, pontos de início/fim, e nós visitados. Essencial para fornecer uma interface visual intuitiva ao usuário.

#### datetime
  Usada para gerar timestamps únicos ao salvar arquivos de labirinto em JSON ou TXT. Isso garante que cada arquivo exportado tenha um nome diferente baseado na data e hora de geração.

#### networkx
  Biblioteca principal para representação do labirinto como grafo. Utilizada para criar os vértices e arestas entre as células da matriz e permitir operações como encontrar vizinhos (graph.neighbors). Também permite adicionar pesos nas arestas, usados pelos algoritmos de busca.

#### random
  Usada para gerar o labirinto aleatoriamente, atribuindo probabilidades de bloqueio (obstáculos) para cada célula. Ajuda a criar diferentes configurações de labirinto a cada execução, tornando os testes mais variados.
  
#### os
  Utilizada para criar diretórios automaticamente ao salvar labirintos exportados (labirintos/). Também serve para manipular caminhos de forma robusta e multiplataforma.

#### json
  Responsável por serializar a matriz do labirinto para o formato JSON, o que facilita a exportação e posterior reutilização dos dados em outros projetos ou linguagens de programação.

#### heapq
  Usada para implementar a fila de prioridade em A* e Dijkstra. Permite escolher sempre o nó com menor custo estimado (no caso do A*) ou menor distância (no caso do Dijkstra), garantindo a eficiência dos algoritmos.

#### time
  Utilizada para medir o tempo de execução dos algoritmos de busca (A* e Dijkstra). Serve para comparações de desempenho e análise da eficiência do caminho encontrado.


  
