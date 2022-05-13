# python3

class Edge:

    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0


class FlowGraph:

    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to, capacity):
        forward_edge = Edge(from_, to, capacity)
        backward_edge = Edge(to, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow


def findAPath(graph, from_, to, ids):
    queue = [[from_]]
    visits = [[0] * (to + 1)]
    tempIds = []
    while len(queue) > 0:
        tempPath = queue[0]
        currentVertex = tempPath[-1]
        del queue[0]
        tempVisit = visits[0]
        tempVisit[currentVertex] = 1
        del visits[0]
        if len(ids) > 0:
            tempIds = ids[0]
            del ids[0]
        if currentVertex == to:
            return tempPath, tempIds
        else:
            for i in graph.graph[currentVertex]:
                if graph.edges[i].capacity - graph.edges[i].flow > 0:
                    if tempVisit[graph.edges[i].v] == 0:
                        queue.append(tempPath + [graph.edges[i].v])
                        visits.append(tempVisit)
                        ids.append(tempIds + [i])
    return [], []


def max_flow(graph, from_, to, matching, n):
    while (True):
        path, ids = findAPath(graph, from_, to, [])
        if len(path) == 0:
            break
        for i in range(1, len(path) - 1):
            if ids[i] % 2 == 0:
                flw = graph.edges[ids[i]].capacity - graph.edges[ids[i]].flow
            else:
                flw = graph.edges[ids[i]].capacity + graph.edges[ids[i]].flow
            if flw > 0 and i + 2 <= len(path) - 1:
                matching[path[i] - 1] = path[i + 1] - n - 1
            graph.add_flow(ids[i - 1], 1)
        graph.add_flow(ids[i], 1)
    return matching


class MaxMatching:
    def read_data(self):
        unassign = []
        n, m = map(int, input().split())
        graph = FlowGraph(m + n + 2)
        flag = True
        for i in range(n):
            li = list(map(int, input().split()))
            if len(li) == li.count(1):
                unassign.append(i)
                continue
            graph.add_edge(0, i + 1, 1)
            for j in range(m):
                if li[j] == 1:
                    graph.add_edge(i + 1, n + j + 1, 1)
                if flag:
                    graph.add_edge(n + j + 1, m + n + 1, 1)
            if flag:
                flag = False
        return graph, n, m, unassign

    def write_response(self, matching):
        line = [str(-1 if x == -1 else x + 1) for x in matching]
        print(' '.join(line))

    def solve(self):
        graph, n, m, unassign = self.read_data()
        matching = [-1] * n
        matching = max_flow(graph, 0, graph.size() - 1, matching, n)
        for i in range(len(unassign) - 1, -1, -1):
            for j in range(m):
                if j not in matching:
                    matching[unassign[i]] = j
                    break
        self.write_response(matching)


if __name__ == '__main__':
    max_matching = MaxMatching()
    max_matching.solve()
