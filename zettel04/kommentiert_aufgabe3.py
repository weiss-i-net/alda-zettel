def archimedes1(k):
    s = 2**0.5
    t = 2       # starting values for a square (n = 4)
    n = 4 * 2**k
    
    for _ in range(k):
        s = ( 2 - (4 - s**2)**0.5 )**0.5
        t = 2/t * ( (4 + t**2)**0.5 - 2 )                                      # comment: Um das Teilen durch 0 zu vermeiden, kann für t im Teiler
                                                                               #          max(t, 1e-15) verwendet werden.
    lower = n/2*s
    upper = n/2*t
    print(f"n: {n}\n{lower} < pi < {upper}\ndelta: {upper - lower}")

    return s, t

archimedes1(23)

#       b)
#
# Ab k = 15 ist delta < 0, ab k = 24 bewegt sich das Ergebinss von pi weg, bei
# k = 27 kommt 4 < pi < 0 raus. Ab k = 28 gibt es einen divison by zero Fehler.
#
# Der Grund für das Verhalten ist, dass bei der Brechnung für kleine s und t
# zwei fast gleiche Zahlen subtrahiert werden (2 und sqrt(4-s^2),
# sqrt(4 + t^2) und 2). Hierdurch kommt es zur Auslöschung, d.h. für jede Stelle
# die gleich ist, geht eine signifikante Stelle in der Gleitkommazahl verloren.
# Ab k = 24 sind die übrig gebliebenen signifikanten Stellen nur noch
# Rundungsfehler durch die begrenzte Präzision von floats.
#
#
#       c)
#
# (Rechnung siehe aufgabe3.pdf)

def archimedes2(k):
    s = 2**0.5
    t = 2       # starting values for a square (n = 4)
    n = 4 * 2**k
    
    for _ in range(k):
        s = s / ( 2 + (4 - s**2)**0.5 )**0.5
        t = 2*t / ( (4 + t**2)**0.5 + 2 )
    
    lower = n/2*s
    upper = n/2*t
    print(f"n: {n}\n{lower} < pi < {upper}\ndelta: {upper - lower:e}")
    
    return s, t

archimedes2(100)

# Die neuen Formeln vermeiden das Subtrahieren fast gleich großer Zahlen und
# somit die Auslöschung.

for i in range(10):
    archimedes2(i)

# Pro Verdoppelung werden ca. 0.6 Dezimalstellen gewonnen.
#
#
#       d)
# 
# (Rechnung siehe aufgabe3.pdf)

# Checks if diffrence between formular and function return of t is less then
# 1^-10
def archimedes_test(st):
    s, t = st[0], st[1]
    return True if t <= 2*s / (4 - s**2)**0.5 + 1e-10 else False               # comment: Hier hätte abs() verwendet werden sollen.

i = 0
while archimedes_test(archimedes1(i)):                                         # comment: Statt geschachtelten Funktionsaufrufen hätte man das mit lambdas
    i += 1                                                                     #          übersichtlicher lösen können.
print(f"Test failed at k={i}")

i = 0
while archimedes_test(archimedes2(i)):
    i += 1
    if i >= 100:
        break
print(f"Test failed at k={i}")

# (Bonusaufgabe siehe bonusaufgabe.pdf)
