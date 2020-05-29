# c)

#       sqrt() befindet sich in math

# Import:
import math

# Verwendung:
print( math.sqrt( 1729**2  ) )



#       sqrt() von einer negativen Zahl wirft eine exception:                   # comment:  Exception-Name: ValueError:  math domain error

try:
    math.sqrt( -1 )
except:
    print( "Exception was thrown" )



#       mysqrt()

def mysqrt1( x ):
    if x < 0:
        print( "mysqrt1() funktioniert nicht für negative Zahlen, du Dussel!" )
    else:
        return math.sqrt( x )

def mysqrt2( x ):
    try:
        return math.sqrt( x )
    except:                                                                     # comment:  "except ValueError:" erlaubt einfacheres Debuggen, wenn mehrere Exceptions im
        print( "mysqrt1() funktioniert nicht für negative Zahlen, du Dussel!" ) #                                try-block geworfen werden

print( mysqrt1( 869765 ) )
print( mysqrt2( 797598 ) )
print( mysqrt1( -1 ) )
print( mysqrt2( -1 ) )



#       Schleife

for i in range( -10, 11 ):
    print( i, i % 5 )

# Der Modulo-Operator gibt den Rest beim Teilen durch eine Zahl an,
# z.B. 9 / 5 == 1 mit Rest 4   <->   9 % 5 == 4
# Die Ausgabe der Schleife wiederholt die Folge 0 1 2 3 4, weil das die
# möglichen Werte für den Rest beim Teilen durch 5 sind.



#       ''' Verwendet man für um Strings über mehrere Zeilen zu schreiben       # comment:  ''' wird Hauptsächlich für doc-strings verwendet

print( '''Beispiel-
string über mehrere
Zeilen.''' )



#       Unterschied List und Dict
#
# List ist ein Array auf dessen Elemente mit einem Index zugegriffen wird.
# Dict ist ein Container, in dem Schlüssel-Wert-Paare abgespeichert sind. Auf
# einen Wert kann man nur mit dem passenden Schlüssel (welcher einen
# beliebigen Datentyp hat) zugreifen.

lissy = [ 'a', "abc", 1, 1.0 ] # List
print( lissy[0] ) # Zugriff per Index

dictty = { "bla" : 10**100,
        9.00001 : True,
        0xABC88F : 0b10111 } # Dict

print( dictty[9.00001] ) # Zugriff per Schlüssel



#       __init__()-Funktion                                                     # comment:  init ist nur der ein Teil des Konstruktors eines Objekts, es wird nach der
#                                                                               #           Erschaffung zur Initialisierung aufgerufen
# Die Init-Funktion ist der Constructor einer Klasse, sie wird bei erstellen    #           __new__() erschafft das Objekt
# eines Objekts aufgerufen. Sie wird benutzt um z.B. interne Variablen zu
# setzen.

class Classy:
    def __init__( self, a, b, c ):
        self.a = a**b
        self.c = c
        print( f"Classy wird mit a={ self.a } und c={ self.c } instanziiert" )

jop = Classy( 10, 100, 1729 )



# d)
#       siehe sieve.py

with open( "sieve.py" ) as fp:
    exec( fp.read() )
primes = sieve( 1000 )
print( primes )

# Output:
#
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
# 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
# 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
# 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
# 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
# 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
# 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607,
# 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
# 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811,
# 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911,
# 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
