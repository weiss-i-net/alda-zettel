# Wenn ein Buchstabe an der Stelle i um n erhöht wird, dann kann man erreichen,
# dass der Hashwert gleich bleibt, in dem man den Buchstaben an der Stelle i+1
# um 23 * n verringert.
# Also sind z.B. " ~" und  "!g" gleichwertig.
#              (32, 126)  (33, 103)

# Mit den 126 - 32 = 94 üblichen Buchstaben, Zahlen und Satzzeichen sind für
# das letzte Zeichen 94/23 + 1 = 5 Zeichen mit Abstand 23 möglich.
# Wenn man für die ersten und letzten zwei Zeichen auf diese Weise je 4
# Kombinationen schafft, hat man insgesamt 16 Kombinationen.

# A = [" ~", "!g", ""P", "#9"] mit Hashwert 862

# Lösung = A x A = [" ~ ~", " ~!g", " ~"P", ...] mit Hashwert 456860

def hhash(s):
    h = 0
    for k in s:
        h = 23*h + ord(k)
    return h

A = [' ~', '!g', '\"P', '#9']

collisons = [ x + y for x in A for y in A ]

for i in collisons:
    assert hhash(i) == 456860

with open('collisons.txt', 'w') as file:
    file.write('\n'.join(collisons))
