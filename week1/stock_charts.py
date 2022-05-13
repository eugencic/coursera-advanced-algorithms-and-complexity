# python3

from collections import deque


def even(num):
    return num % 2 == 0


def odd(num):
    return not num % 2 == 0


class Edge:
    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

    def __str__(self):
        return "from={} to={} cap={} flow={}".format(self.u, self.v, self.capacity, self.flow)


class FlowGraph:
    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]

    def print(self):
        for ix, edge in enumerate(self.edges):
            if even(ix):
                print(edge)

    def get_matching(self):
        matching = [-1 for _ in range(self.nflights)]
        for flightid in range(1, self.nflights + 1):
            for edgeid in self.get_ids(flightid)[1:]:
                edge = self.get_edge(edgeid)
                if edge.flow == 1:
                    matching[edge.u - 1] = edge.v - self.nflights
        return matching

    def add_edge(self, from_, to, capacity):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
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
        # To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
        # due to the described above scheme. On the other hand, when we have to get a "backward"
        # edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
        # should be taken.
        #
        # It turns out that id ^ 1 works for both cases. Think this through!
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow

    def saturated(self, edgeid):
        return self.get_edge(edgeid).flow == self.get_edge(edgeid).capacity

    def edmunds_karp_BFS(self):
        explored = [False for _ in range(self.size())]
        parents = [None for _ in range(self.size())]
        pedges = [None for _ in range(self.size())]
        stack = deque([0])
        while stack:
            nodeid = stack.pop()
            explored[nodeid] = True
            for edgeid in self.get_ids(nodeid):
                u_node = self.get_edge(edgeid).u
                v_node = self.get_edge(edgeid).v
                if (even(edgeid) and not self.saturated(edgeid) and not explored[v_node]) \
                        or (odd(edgeid) and self.edges[edgeid].flow < 0 and not explored[v_node]):
                    stack.appendleft(v_node)
                    parents[v_node] = u_node
                    pedges[v_node] = edgeid
                    if v_node == self.size() - 1:
                        path_node = v_node
                        path = [path_node]
                        edge_path = []  # Always one less edge than node along a path
                        while True:
                            path.append(parents[path_node])
                            edge_path.append(pedges[path_node])
                            path_node = parents[path_node]
                            if path_node == 0:
                                return path, edge_path
        return None, None

    def max_flow(self, from_, to):
        total_flow = 0
        while True:
            node_path, edge_path = self.edmunds_karp_BFS()
            if node_path is None:
                break
            glst = []
            for edgeid in edge_path:
                if even(edgeid):
                    glst.append(self.get_edge(edgeid).capacity - self.get_edge(edgeid).flow)
                else:
                    glst.append(-self.get_edge(edgeid).flow)
            maxg = min(glst)
            for edgeid in edge_path:
                self.add_flow(edgeid, maxg)
                if self.get_edge(edgeid).v == to:
                    total_flow += maxg
        return total_flow


class StockCharts:
    def read_data(self):
        n, k = map(int, input().split())
        stock_data = [list(map(int, input().split())) for i in range(n)]
        return stock_data

    def make_flow_graph(self, stock_data):
        n = len(stock_data)
        k = len(stock_data[0])
        vertex_count = 2 * n + 2
        graph = FlowGraph(vertex_count)
        # Connect the source to the left bipartite
        for stock in range(n):
            graph.add_edge(0, stock + 1, 1)
        for ix, istock in enumerate(stock_data):
            for jx, jstock in enumerate(stock_data):
                if all([a < b for a, b in zip(jstock, istock)]):
                    graph.add_edge(ix + 1, n + 1 + jx, capacity=1)
        # Connect the right bipartite to the sink
        for stock in range(n):
            graph.add_edge(n + 1 + stock, vertex_count - 1, 1)
        return graph

    def write_response(self, result):
        print(result)

    def min_charts_naive(self, stock_data):
        # Replace this incorrect greedy algorithm with an
        # algorithm that correctly finds the minimum number
        # of charts on which we can put all the stock data
        # without intersections of graphs on one chart.
        n = len(stock_data)
        k = len(stock_data[0])
        charts = []
        for new_stock in stock_data:
            added = False
            for chart in charts:
                fits = True
                for stock in chart:
                    above = all([x > y for x, y in zip(new_stock, stock)])
                    below = all([x < y for x, y in zip(new_stock, stock)])
                    if (not above) and (not below):
                        fits = False
                        break
                if fits:
                    added = True
                    chart.append(new_stock)
                    break
            if not added:
                charts.append([new_stock])
        return len(charts)

    def min_charts(self, stock_data):
        graph = self.make_flow_graph(stock_data)
        total_flow = graph.max_flow(0, graph.size() - 1)
        return len(stock_data) - total_flow

    def solve(self):
        stock_data = self.read_data()
        result = self.min_charts(stock_data)
        self.write_response(result)


if __name__ == '__main__':
    stock_charts = StockCharts()
    stock_charts.solve()
