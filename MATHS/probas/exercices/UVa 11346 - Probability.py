import math

for _ in range(int(input())):
    a, b, S = map(float,input().split())
    if a * b <= S:
        ans = 0
    elif S == 0:
        ans = 1
    else:
        area = S * (1 + math.log(a) - math.log((S / b) + 1e-9)) # pour éviter erreur log(0)
        ans = 1 - (area / (a * b))
    print("{:.06f}%".format(ans * 100))

"""
The probability P is essentially the ratio of the area where |X|⋅|Y| > S to the total area of the region A.
Since A is a rectangle centered at the origin, it’s symmetric with respect to both axes.
Thus, we can focus on just the first quadrant (where X and Y are both positive).
To calculate the area under the curve X⋅Y=S within the first quadrant up to the bounds X∈[0,a] and Y∈[0,b],
we can use integration. However, the solution uses an approximation based on logarithmic functions.
For a fixed value of S, the region bounded by X⋅Y≤S can be approximated by S ⋅ (1 + log(a) - log(S/b))
S: This factor represents scaling of the region’s area due to the threshold S
log(a): This term accounts for the width of the region along the X-axis, up to x=a.
log(S/b): This term adjusts for the bounds of Y, reflecting that as S changes, the Y-limit on the region also shifts.

P(|X|⋅|Y| > S) = 1 - (4⋅S⋅(1 + log(a) - log(S/b))) / (4⋅a⋅b) = 1 - S⋅(1 + log(a) - log(S/b)) / (a⋅b)
"""