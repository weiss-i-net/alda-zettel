import random
import math
import numpy as np
from copy import deepcopy
import pytest
import timeit
def create_data(size):
    a = []
    while len(a) < size:
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        r = math.sqrt(x**2 + y**2)
        if r < 1.0: # der Punkt (x,y) liegt im Einheitskreis
            a.append(r)
    return a

#
# a = create_data(10)
#
#
# # print(len(a))
#


def quantize(r, M):
    # This is the original implement of the index. But this will cause the
    # index not equally distributed
    return int(r*M)


# Aufgabe a)
# 𝐹(𝑟) = 𝑃(𝑟′ < 𝑟) = The circle with radius r' / The circle with the radius 1 = πr'**2 / π = r'**2
# From this equation we can see, that the probability of large radius increases with r'²
# they are therefore much more likely than small ones and the int (r * M) can not lead to an equal distribution.
# And the new_quantize below will do the work that we want

def new_quantize(r, M):
    # This shall be the right formula for a equal distribution.
    return int(r ** 2 * M)


def chi_squared(buckets):
    bucket_lens = [len(q) for q in buckets] # The length of each bucket
    N = len(a)  # The key size is the length of a
    M = len(bucket_lens)
    c_mean = float(N) / M
    chi_value = 0.0
    for k in bucket_lens:
        chi_value += (k - c_mean)**2 / c_mean
    p = np.sqrt(2.0*chi_value) - np.sqrt(2.0*M-3.0)
    if p<=3:
        return True
    else:
        return False

def insertionSort(b):
    # prepared to be used in bucketSort
    N = len(b)
    for k in range(1, N):
        v = b[k]
        j = k
        while j > 0 and b[j - 1] > v:
            b[j] = b[j - 1]
            j -= 1
        b[j] = v


def bucket_sort(a, bucketMap, d=3.0):
    N = len(a)
    M = int(math.floor(N / d)) + 1
    buckets = [[] for k in range(M)]
    for k in a:
        buckets[bucketMap(k, M)].append(k)
    i = 0
    for k in buckets:
        insertionSort(k)
        a[i:i + len(k)] = k
        i += len(k)
    return buckets

# mini test for the chi square
for n in range(100,300,50):
    a = create_data(n)
    bucket1 = bucket_sort(a,quantize)
    buckets2 = bucket_sort(a,new_quantize)
    print(('n = '+ str(n) + '\t original formel: ' + str(chi_squared(bucket1))))
    print(('n = ' + str(n) + '\t our formel: ' + str(chi_squared(buckets2))))

# The result is like:
# n = 100	 original formel: False
# n = 100	 our formel: True
# n = 150	 original formel: False
# n = 150	 our formel: True
# n = 200	 original formel: False
# n = 200	 our formel: True
# n = 250	 original formel: False
# n = 250	 our formel: True

@pytest.fixture()
def test_bucket_sort():
    #Test for the bucket sort
    for n in range(100,300,50):
        a = create_data(n)
        copy_original = deepcopy(a)
        copy_original.sort()
        bucket = bucket_sort(original, new_quantize)
        assert bucket == copy_original




for n in range(100,300,50):
    a = create_data(n)
    print("The original formel: "+str(timeit.timeit("bucket_sort(a,quantize)", globals=globals())))
    print("Our formel: "+str(timeit.timeit("bucket_sort(a,new_quantize)", globals=globals())))

# The result is like this.
#The original formel: 42.4547134999998
# Our formel: 49.386994799999684
# The original formel: 65.26414609999983
# Our formel: 71.14930159999994
# The original formel: 81.45010300000013
# Our formel: 93.06738610000002
# The original formel: 103.73055360000035
# Our formel: 113.27601159999995
# Based on these data, we can say that their growth is basically linear.
