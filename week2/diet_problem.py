# python3

from sys import stdin

EPS = 1e-6
PRECISION = 20


class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row


def ReadEquation():
    size = int(input())
    a = []
    b = []
    for row in range(size):
        line = list(map(float, input().split()))
        a.append(line[:size])
        b.append(line[size])
    return Equation(a, b)


def SelectPivotElement(a, used_rows, used_columns):
    pivot_element = Position(0, 0)
    while used_rows[pivot_element.row]:
        pivot_element.row += 1
    while used_columns[pivot_element.column] or a[pivot_element.row][pivot_element.column] == 0:
        pivot_element.column += 1
        if pivot_element.column > len(used_columns) - 1:
            return False
    return pivot_element


def SwapLines(a, b, used_rows, pivot_element):
    a[pivot_element.column], a[pivot_element.row] = a[pivot_element.row], a[pivot_element.column]
    b[pivot_element.column], b[pivot_element.row] = b[pivot_element.row], b[pivot_element.column]
    used_rows[pivot_element.column], used_rows[pivot_element.row] = used_rows[pivot_element.row], used_rows[
        pivot_element.column]
    pivot_element.row = pivot_element.column


def ProcessPivotElement(a, b, pivot_element):
    divisor = a[pivot_element.row][pivot_element.column]
    a[pivot_element.row] = [x / divisor for x in a[pivot_element.row]]
    b[pivot_element.row] = b[pivot_element.row] / divisor
    for i in range(len(a)):
        if i == pivot_element.row:
            continue
        if a[i][pivot_element.column] != 0:
            factor = a[i][pivot_element.column]
            a[i] = [x - factor * y for x, y in zip(a[i], a[pivot_element.row])]
            b[i] = b[i] - factor * b[pivot_element.row]


def MarkPivotElementUsed(pivot_element, used_rows, used_columns):
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True


def compare_LE(a, b):
    return round(a, 5) <= round(b, 5)


def CheckInequalities(A, b, x):
    bcheck = [0 for _ in range(len(b))]
    for i in range(len(A)):
        bcheck[i] = sum([a * x_ for a, x_ in zip(A[i], x)])
    return all([compare_LE(x, y) for x, y in zip(bcheck, b)])


def SolveEquation(equation):
    a = equation.a[:]
    b = equation.b[:]
    size = len(a)

    used_columns = [False] * size
    used_rows = [False] * size
    problem = False
    for step in range(size):
        pivot_element = SelectPivotElement(a, used_rows, used_columns)
        if not pivot_element:
            problem = True
            break
        SwapLines(a, b, used_rows, pivot_element)
        ProcessPivotElement(a, b, pivot_element)
        MarkPivotElementUsed(pivot_element, used_rows, used_columns)
    if problem:
        return False
    return b


def make_subsets(n, m):
    a = [(), (0,)]
    for i in range(1, n + m + 1):
        newa = a.copy()
        for x in newa:
            a.append(x + (i,))
    a = [y for y in a if len(y) == m]
    return a


def solve_diet_problem(n, m, A, b, c):
    best_satisfaction = -float('inf')
    best_solution = None
    no_solutions = True
    for subset in make_subsets(n, m):
        eqn = Equation([A[i] for i in subset], [b[i] for i in subset])
        x = SolveEquation(eqn)
        if x and CheckInequalities(A, b, x):
            no_solutions = False
            satisfaction = sum([c_ * x_ for c_, x_ in zip(c, x)])
            if satisfaction > best_satisfaction:
                best_satisfaction = satisfaction
                best_solution = x
    if no_solutions:
        return [-1, False]
    if sum(best_solution) > (10 ** 9 - 1):
        return [1, False]
    else:
        return [0, best_solution]


n, m = list(map(int, stdin.readline().split()))
A = []
for i in range(n):
    A += [list(map(int, stdin.readline().split()))]
b = list(map(int, stdin.readline().split()))
for i in range(m):
    A += [[-1 if i == j else 0 for j in range(m)]]
A += [[1 for _ in range(m)]]
b += [0 for j in range(m)]
b += [10 ** 9]
c = list(map(int, stdin.readline().split()))

anst, ansx = solve_diet_problem(n, m, A, b, c)

if anst == -1:
    print("No solution")
if anst == 0:
    print("Bounded solution")
    print(' '.join(list(map(lambda x: '%.18f' % x, ansx))))
if anst == 1:
    print("Infinity")
