def arithm_expr_eval(cell, expr):
    """Evaluates a given expression

    :param expr: expression
    :param cell: dictionary variable name -> expression

    :returns: numerical value of expression

    :complexity: linear
    """
    if isinstance(expr, tuple):
        (left, operand, right) = expr
        lval = arithm_expr_eval(cell, left)
        rval = arithm_expr_eval(cell, right)
        if operand == '+':
            return lval + rval
        if operand == '-':
            return lval - rval
        if operand == '*':
            return lval * rval
        if operand == '/':
            return lval // rval
    elif isinstance(expr, int):
        return expr
    else:
        cell[expr] = arithm_expr_eval(cell, cell[expr])
        return cell[expr]

PRIORITY = {';': 0, '(': 1, ')': 2, '-': 3, '+': 3, '*': 4, '/': 4}

def arithm_expr_parse(line_tokens):
    """Constructs an arithmetic expression tree

    :param line_tokens: list of token strings containing the expression
    :returns: expression tree

    :complexity: linear
    """
    vals = []
    ops = []
    for tok in line_tokens + [';']:
        if tok in PRIORITY:  # tok is an operator
            while (tok != '(' and ops and
                   PRIORITY[ops[-1]] >= PRIORITY[tok]):
                right = vals.pop()
                left = vals.pop()
                vals.append((left, ops.pop(), right))
            if tok == ')':
                ops.pop()    # this is the corresponding '('
            else:
                ops.append(tok)
        elif tok.isdigit():  # tok is an integer
            vals.append(int(tok))
        else:                # tok is an identifier
            vals.append(tok)
    return vals.pop()

for _ in range(int(input())):
    cell = {}
    input()
    for _ in range(int(input())):
        line = input().rstrip('\n').split()
        cell[line[0]] = arithm_expr_parse(line[2:])
    for lhs in sorted(cell.keys()):
        print("{} = {}".format(lhs, arithm_expr_eval(cell, lhs)))
    print()

"""
INPUT:
1

3
A47 = 5 + ZZ22
ZZ22 = 3
A9 = 13 + A47 * ZZ22

OUTPUT:
A47 = 8
A9 = 37
ZZ22 = 3

"""

# SOLVE 3+2*10/x=100/10+3 FOR X

a, b = input().split('=')

if 'x' in b:
    a, b = b, a

res = eval(b)

for j in range(a.find('x') - 1, -1, -1):
    if a[j] in '+-':
        if a[j] == '+': res -= eval(a[:j])
        else: res += eval(a[:j])
        a = a[j + 1:]
        break
for j in range(a.find('x') + 1, len(a)):
    if a[j] in '+-':
        if a[j] == '+': res -= eval(a[j + 1:])
        else: res += eval(a[j + 1:])
        a = a[:j]
        break

assert '+' not in a
assert '-' not in a

i = a.find('x')
if i - 1 >= 0:
    if a[i - 1] == '/':
        res = eval(a[:i - 1]) / res
    else:
        res /= eval(a[:i - 1])
if i + 1 < len(a):
    if a[i + 1] == '/':
        res *= eval(a[i + 2:])
    else:
        res /= eval(a[i + 2:])

print(res)