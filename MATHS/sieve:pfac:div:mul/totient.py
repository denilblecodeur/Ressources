# counts the positive integers up to n that are relatively prime to n
def totient(n):
    res = 1
    for p, a in pfac(n).items():
        res *= pow(p, a - 1) * (p - 1)
    return res

def sum_coprimes(n):
    return (totient(n) * n) // 2