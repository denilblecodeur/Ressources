#Pythagorean Pair
from math import sqrt


def solution(num):
    divs = 0
    while num % 2 == 0:
        divs+=1 
        num //= 2
    if divs % 2 == 1:
        num*=2
        divs-=1
    i=0
    while i*i <= num:
        var = num - (i*i)
        temp = int(sqrt(var))
        if temp*temp == var:
            print( i << (divs//2), temp << (divs//2))
            return
        i+=1
    print(-1)

testcases = int(input())
for i in range (testcases):
    solution(int(input()))