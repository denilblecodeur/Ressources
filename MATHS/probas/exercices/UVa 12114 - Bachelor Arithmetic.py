import sys

tc = 0
for line in sys.stdin.buffer:
    tc += 1
    B, S = map(int,line.split())
    if B == S == 0: break
    ans = ":-"
    if (B-1) == 0:
        ans += '\\'
    elif (S-1) * B == S * (B-1):
        ans += '|'
    elif (S-1) * B > S * (B-1):
        ans += ')' if S < B else '|'
    else:
        ans += '(' if (S-1) < (B-1) else '|'
    print("Case {}: {}".format(tc, ans))