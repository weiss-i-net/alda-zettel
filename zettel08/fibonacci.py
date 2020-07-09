import time
import pytest

def fib1(n):
    if n <= 1:
        return n
    return fib1(n-1) + fib1(n-2)

def fib3_impl(n):
    if n == 0:
        return 1, 0
    f1, f2 = fib3_impl(n-1)
    return f1 + f2, f1

def fib3(n):
    return fib3_impl(n)[1]

def fib5(n):
    fib = [0, 1]
    for _ in range(n - 1):
        fib.append(fib[-1] + fib[-2])
    return fib[n]

def find_biggest_n(fib_function, max_time=10):
    start_time = time.time()
    n = 0
    while time.time() - start_time < max_time:
        n += 1
        try:
            fib_function(n)
        except RuntimeError:
            break
    return n


class Matrix2x2:
    def __init__(self, *init_list):
        self.data = init_list
    def __mul__(self, other):
        return Matrix2x2( self.data[0]*other.data[0] + self.data[1]*other.data[2],
                          self.data[0]*other.data[1] + self.data[1]*other.data[3],
                          self.data[2]*other.data[0] + self.data[3]*other.data[2],
                          self.data[2]*other.data[1] + self.data[3]*other.data[3] )
    def __str__(self):
        return str(self.data[:2]) + '\n' + str(self.data[2:])

IDENTIY_MATRIX = Matrix2x2(1, 0, 0, 1)

class Matrix2x2BadPow(Matrix2x2):
    def __pow__(self, n):
        return_matrix = IDENTIY_MATRIX
        for _ in range(n):
            return_matrix *= self
        return return_matrix

class Matrix2x2BetterPow(Matrix2x2):
    @staticmethod
    def _recu_pow(matrix, n):
        if n == 0:
            return IDENTIY_MATRIX
        if n == 1:
            return matrix
        if n & 1:
            return matrix * Matrix2x2BetterPow._recu_pow(matrix * matrix, (n-1)//2)
        return Matrix2x2BetterPow._recu_pow(matrix * matrix, n//2)

    def __pow__(self, n):
        return self._recu_pow(self, n)

def fib6(N):
    return (Matrix2x2BadPow(1, 1, 1, 0)**N).data[1]

def fib7(N):
    return (Matrix2x2BetterPow(1, 1, 1, 0)**N).data[1]

@pytest.mark.parametrize('fib_func', [fib1, fib3, fib5, fib6, fib7])
def test_fib(fib_func):
    for n, fib_n in [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (20, 6765)]:
        assert fib_func(n) == fib_n

def main():
    print(f'Biggest n for fib1: {find_biggest_n(fib1)}')
    # Small result because of exponential behavior (37).

    print(f'Biggest n for fib3: {find_biggest_n(fib3)}')
    # 997 because thats the max. recursion depth

    print(f'Biggest n for fib5: {find_biggest_n(fib5)}')
    # Big result because of efficient (linear) calculation and no recursion, so
    # no recursion depth limit (9063)

    print(f'Biggest n for fib6: {find_biggest_n(fib6)}')
    # Smaller result than fib5 because even though this is linear as well, matrix
    # multiplication is more costly then simple addition. (3869)

    print(f'Biggest n for fib7: {find_biggest_n(fib7)}')
    # Biggest result because of the logarithmic behavior of the more efficient
    # matrix power. (284336)


if __name__=='__main__':
    main()
