def sieve( n ):
    candidates = range( 2, n )
    for prime in candidates:
        candidates = [ i for i in candidates if i not in range( prime * 2, n, prime ) ]  # comment:  Man sollte nicht über eine Liste iterieren die man in der for-Schleife
    return candidates                                                                    #           ändert, da es zu unvorhergesehenem Verhalten führen kann.
                                                                                         #           Stattdessen sollte man mit einem Index über die Liste iterieren.
