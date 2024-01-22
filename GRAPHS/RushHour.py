import sys
from collections import deque

n = int(input())

orientat, longueur, coorfixe, coorvari = [-1]*n, [-1]*n, [-1]*n, [-1]*n

coor_id = {}

for i in range(n):
    _id, x, y, length, axis = map(int,input().replace('H','0').replace('V','1').split())
    coor_id[i] = _id
    orientat[i] = axis
    longueur[i] = length
    coorfixe[i] = x if axis > 0 else y
    coorvari[i] = y if axis > 0 else x

assert orientat.count(-1) == longueur.count(-1) == coorfixe.count(-1) == coorvari.count(-1) == 0

def someCarIsHere(x,y,cvari):
    for i in range(n):
        if orientat[i] == 0 and coorfixe[i] == y and cvari[i] <= x <= cvari[i] + longueur[i] - 1:
            return True
        if orientat[i] == 1 and coorfixe[i] == x and cvari[i] <= y <= cvari[i] + longueur[i] - 1:
            return True
    return False

answer = None
queue = deque([(coorvari,[])])
asConfigs = set()

while queue:
    current_coorvari, road = queue.popleft()

    if current_coorvari[0] == 4:
        answer = road
        break
    
    for car in range(n):
        #case + 1
        x = coorfixe[car] if orientat[car] == 1 else current_coorvari[car] + longueur[car]-1 + 1
        y = current_coorvari[car] + longueur[car]-1 + 1 if orientat[car] == 1 else coorfixe[car]

        if x < 6 and y < 6 and not someCarIsHere(x,y,current_coorvari):
            current_coorvari[car] += 1
            newroad = road + [(car,'DOWN') if orientat[car] == 1 else (car,'RIGHT')]
            hashed = hash(''.join(map(str,current_coorvari)))
            if hashed not in asConfigs:
                queue.append((current_coorvari[:],newroad))
                asConfigs.add(hashed)
            current_coorvari[car] -= 1

        #case - 1
        x = coorfixe[car] if orientat[car] == 1 else current_coorvari[car] - 1
        y = current_coorvari[car] - 1 if orientat[car] == 1 else coorfixe[car]

        if x >= 0 and y >= 0 and not someCarIsHere(x,y,current_coorvari):
            current_coorvari[car] -= 1
            newroad = road + [(car,'UP') if orientat[car] == 1 else (car,'LEFT')]
            hashed = hash(''.join(map(str,current_coorvari)))
            if hashed not in asConfigs:
                queue.append((current_coorvari[:],newroad))
                asConfigs.add(hashed)
            current_coorvari[car] += 1

answer = ((coor_id[i],DIR) for i,DIR in answer)