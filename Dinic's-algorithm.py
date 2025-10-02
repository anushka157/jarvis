from collections import deque

class Edge:
    def __init__(self, v, capacity, rev):
        self.v = v               # target vertex
        self.capacity = capacity # remaining capacity
        self.rev = rev           # index of reverse edge

class Dinic:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]

    def add_edge(self, u, v, capacity):
        forward = Edge(v, capacity, len(self.graph[v]))
        backward = Edge(u, 0, len(self.graph[u]))
        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def bfs(self, s, t, level):
        q = deque([s])
        level[s] = 0
        while q:
            u = q.popleft()
            for e in self.graph[u]:
                if e.capacity > 0 and level[e.v] < 0:
                    level[e.v] = level[u] + 1
                    q.append(e.v)
        return level[t] >= 0

    def send_flow(self, u, flow, t, start, level):
        if u == t:
            return flow
        while start[u] < len(self.graph[u]):
            e = self.graph[u][start[u]]
            if e.capacity > 0 and level[e.v] == level[u] + 1:
                curr_flow = min(flow, e.capacity)
                temp_flow = self.send_flow(e.v, curr_flow, t, start, level)
                if temp_flow > 0:
                    e.capacity -= temp_flow
                    self.graph[e.v][e.rev].capacity += temp_flow
                    return temp_flow
            start[u] += 1
        return 0

    def max_flow(self, s, t):
        total = 0
        while True:
            level = [-1] * self.n
            if not self.bfs(s, t, level):
                break
            start = [0] * self.n
            while True:
                flow = self.send_flow(s, float('inf'), t, start, level)
                if flow == 0:
                    break
                total += flow
        return total


# Example usage:
if __name__ == "__main__":
    # Graph with 6 nodes (0 = source, 5 = sink)
    n = 6
    dinic = Dinic(n)

    # Add edges (u, v, capacity)
    dinic.add_edge(0, 1, 16)
    dinic.add_edge(0, 2, 13)
    dinic.add_edge(1, 2, 10)
    dinic.add_edge(1, 3, 12)
    dinic.add_edge(2, 1, 4)
    dinic.add_edge(2, 4, 14)
    dinic.add_edge(3, 2, 9)
    dinic.add_edge(3, 5, 20)
    dinic.add_edge(4, 3, 7)
    dinic.add_edge(4, 5, 4)

    print("Maximum flow:", dinic.max_flow(0, 5))  # Expected: 23
