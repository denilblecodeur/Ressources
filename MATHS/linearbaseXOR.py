"""
linearbase
prend une liste de nombres a et renvoie une base linéaire
(un ensemble minimal d’éléments indépendants en termes de bits) pour la liste a.
L'objectif est de créer une représentation réduite où chaque nombre est une combinaison
linéaire unique des nombres dans cette base.

baseinsert
Cette fonction prend une base b et un nombre x, et essaie d’insérer x dans b si cela est possible.
Si x peut être ajouté sans redondance, il est inséré et la fonction renvoie True.
Sinon, elle renvoie False.
"""


mx_bit=20
def linearbase(a):
    res=[0]*mx_bit
    for x in a:
        for i in range(mx_bit-1,-1,-1):
            if x>>i&1:
                if res[i]:
                    x^=res[i]
                else:
                    res[i]=x
                    break
    return res
def baseinsert(b,x):
    for i in range(mx_bit-1,-1,-1):
        if x>>i&1:
            if b[i]:
                x^=b[i]
            else:
                b[i]=x
                return True   
    return False