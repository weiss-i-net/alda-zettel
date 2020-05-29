import math

# 10 cm Schritte
max_h = 30
break_h = 31

def does_it_break(h):
    return True if h >= break_h else False

# a)

h = 1
while not does_it_break(h):
    h += 1

print(f"Glass broke at {h}")

# Man fangt bei der untersten Plattform an und probiert es so lange mit den
# nächst-höheren Plattform bis das Glass zerbricht.
# Es werden maximal 29 Versuch benötigt, da in diesem Fall das Glass bei allen
# Plattformen getestet wird und nicht zerbricht.


# b)

broken_glasses = 0
trys = 0

def recu_test(l, h):
    half = (l + h) // 2
    breaks = does_it_break(half)

    global broken_glasses, trys
    if breaks:
        broken_glasses += 1
    trys += 1

    if half == h:
        return h - 1 if breaks else h
    else:
        return recu_test(l, half - 1) if breaks else recu_test(half + 1, h)

print(f"max. height: {recu_test(1, max_h)}   broke {broken_glasses} glasses"
      f" with {trys} trys.")

# Man fängt bei der mittlern Plattform an. Falls des Glas zerbricht, testet man
# die mittlere Plattform der unteren Hälfte, andernfalls der oberen Hälfte.
# Dieses Verfahren wendet man rekursiv an, bis der betrachtete Bereich aus
# einer Plattform besteht.
# 
# Hierbei wird maximal 5 mal getestet. Allgm.: ceil( log_2( p ) ) wobei p die
# Zahl der Plattformen ist.  Im schlimmsten Fall zerbricht das Glas bei der
# ersten Plattform.  In diesem Fall zerbrechen 5 Gläser. 


# c) d)
#
# Sobald das erste Glass zerbricht, muss für das zweite Glass die Methode aus
# a) verwendet werden.
# Der erste Test muss so gewählt werden, dass der worst-case bei beiden
# Ergebnissen gleich ist.
# Angenommen der worst-case ist x, dann muss der erste Test bei Plattform x
# gemacht werden, weil potentiell alle Plattformen unter x durchprobiert
# werden.
#
# Plattform 1     Test 1        Test 2      Test 3         Plattform 30
#     V             v             v           v                 V
#     | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | 
#     \             / \           / \         /
#      worst case 1:  worst case 2: worst case 3:
#            x         (x-1) + 1     (x-2) + 2
#                              ^ Test 1      ^ Test 1 & 2
#
# Falls das Glas beim ersten Test nicht zerbricht, wird auf der Ebene
# x + (x - 1) getestet, hier ist der worst-case x - 1 für die obere Hälfte
# und + 1 für den ersten Test (= x). Beim folgenden Test wird bei
# x + (x - 1) + (x - 2) getestet. usw.
# Für die Gesamthöhe gilt also:                                                 # comment:  Für die Gesamthöhe h...
#
# h = x + (x - 1) + (x - 2) + ... + 2 + 1                                       # comment:  h wurde ungeschickt gewählt, da es mit anderer Bedutung im Code verwendet wird
#   = x(x + 1) / 2
#
# -> x = (sqrt(8h + 1) - 1) / 2                                                 
#
# Um eine ganzzahlige Plattform zu bekommen wird aufgerundet.
# Die maximale Anzahl der Versuche v abhängig von h ist also:
# v = ceil( (sqrt(8h + 1) - 1) / 2 )

trys = 0
x_0 = x = math.ceil( ( (8*h + 1)**0.5 - 1 ) / 2 )                               # comment:  ...(8*max_h + 1)... 

def a_test(l):
    global trys
    while not does_it_break(l) and l <= h:
        l += 1
        trys += 1
    return l - 1

def b_test(l, h):
    global trys, x
    x += x_0 - trys
    if x > h:
        return h
    trys += 1
    return a_test(l) if does_it_break(x) else b_test(x + 1, h)                  # comment:  h ändert sich nicht und sollte nicht als Argument übergeben werden

def first_test(max_h):
    global trys, x
    trys += 1
    return a_test(1) if does_it_break(x) else b_test(x + 1, max_h)


print(f"max. height: {first_test(max_h)}   {trys} trys.")


# Test der maximalen Versuchszahl:
#
# h = 30: v = 8

max_trys = 0

for i in range(1, 32):
   break_h = i
   trys = 0
   x = x_0
   first_test(30)

   max_trys = trys if trys > max_trys else max_trys

print(f"max_trys: {max_trys}")

# # Output:   max_trys: 8
