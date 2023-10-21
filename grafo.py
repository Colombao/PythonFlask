from flask import Flask, render_template
import heapq
import time
import random


app = Flask(__name__)

def generate_random_graph(nodes):
    graph = {}
    for node in nodes:
        edges = {}
        for neighbor in nodes:
            if neighbor != node:
                edges[neighbor] = random.randint(1, 10)  # Atribui pesos aleatórios de 1 a 10
        graph[node] = edges
    return graph

nodes = ['A', 'B', 'C', 'D']  # Lista de nós do grafo
graph = generate_random_graph(nodes)  # Gera o grafo com pesos aleatórios
start_node = 'A'


def dijkstra(graph, start):
    # Registra o tempo de início da função
    start_time = time.time()

    # Inicializa um dicionário de distâncias com infinito para todos os nós
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time, distances

start_node = 'A'

@app.route('/')
def dijkstra_results():
    elapsed_time, result = dijkstra(graph, start_node)
    return render_template('grafo.html', start_node=start_node, elapsed_time=elapsed_time, result=result)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
