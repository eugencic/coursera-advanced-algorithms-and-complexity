# python3

n, m = map(int, input().split())
edges = [list(map(int, input().split())) for i in range(m)]


# This solution prints a simple formula
# and passes about half of the tests.
# Change this function to solve the problem.
def printEquisatisfiableSatFormula(n, edges):
    for i in range(1, n + 1):
        val = i * 3
        print(-(val - 1), -val, 0)
        print(-(val - 2), -(val - 1), 0)
        print(-(val - 2), -val, 0)
        print((val - 2), (val - 1), val, 0)
    for i, j in edges:
        val1 = i * 3
        val2 = j * 3
        print(-(val1 - 2), (val2 - 1), val2, 0)
        print(-(val1 - 1), (val2 - 2), val2, 0)
        print(-val1, (val2 - 1), (val2 - 2), 0)


print((m * 3 + n * 4), n * 3)
printEquisatisfiableSatFormula(n, edges)
