import time

graph = {'A': ['B', 'C'],
         'B': ['A', 'D', 'E'],
         'C': ['A', 'F'],
         'D': ['B', 'C'],
         'E': ['B', 'F'],
         'F': ['C', 'E']
         }


def bfs(graph, start, end):
    start_time = time.time()

    visited = {start: None}
    queue = [start]
    while queue:
        print("Queue: " + str(queue))
        print("Visited: " + str(visited))
        node = queue.pop(0)
        if node == end:
            path = []
            while node is not None:
                path.append(node)
                node = visited[node]
            return path[::-1]
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited[neighbour] = node
                queue.append(neighbour)

print(bfs(graph, 'A', 'F'))
