def sieve( n ):
    candidates = range( 2, n )
    for prime in candidates:
        candidates = [ i for i in candidates if i not in range( prime * 2, n, prime ) ]
    return candidates

def sieve_high_performance( n ):
    candidates = [ False, True ] * ( n // 2 )
    candidates[1], candidates[2] = False, True
    for i in range(3, int( n**0.5 ) + 1):
        if candidates[i]:
            for o in range(i**2, n, 2*i):
                candidates[o] = False
    return [ i for i, is_prime in enumerate(candidates) if is_prime ]
    
# print( sieve( 100000 )[-10:] )
print( sieve_high_performance( 100000000 )[-10:] )
