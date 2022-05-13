# python3

n, m = map(int, input().split())
edges = [list(map(int, input().split())) for i in range(m)]


# This solution prints a simple formula
# and passes about half of the tests.
# Change this function to solve the problem.
def printEquisatisfiableSatFormula(n, edges):
    li = []
    for i in range(1, n + 1):
        val = i * n
        li.append(' '.join([str((val - x)) for x in range(n)]) + " " + str(0))
        for j in range(n):
            for k in range(j + 1, n):
                li.append(str(-(val - j)) + " " + str(-(val - k)) + " " + str(0))
    for i in range(n):
        li.append(' '.join([str((x * n) - i) for x in range(1, n + 1)]) + " " + str(0))
        for j in range(1, n):
            for k in range(j + 1, n + 1):
                li.append(str(-(j * n - i)) + " " + str(-(k * n - i)) + " " + str(0))
        if i != 0:
            for j in range(i + 1, n + 1):
                if [i, j] not in edges and [j, i] not in edges:
                    for k in range(n - 1):
                        li.append(str(-(i * n - k)) + " " + str(-(j * n - k - 1)) + " " + str(0))
                        li.append(str(-(i * n - k - 1)) + " " + str(-(j * n - k)) + " " + str(0))
    print(len(li), n * n)
    for i in li:
        print(i)


printEquisatisfiableSatFormula(n, edges)
