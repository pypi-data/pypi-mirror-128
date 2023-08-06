from numpy import random
from timeit import timeit
from numexpr import evaluate


if __name__ == '__main__':

    A = random.rand(4000, 4000)
    B = random.rand(4000, 4000)

    def pure_np(m1, m2):

        return m1 * m2

    def with_numexpr(m1, m2):

        return evaluate("m1 * m2", out=m1)

    print(timeit("pure_np(A, B)", globals=globals(), number=100))
    print(timeit("with_numexpr(A, B)", globals=globals(), number=100))
