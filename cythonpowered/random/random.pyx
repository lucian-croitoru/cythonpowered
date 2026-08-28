# -----------------------------------------------------------------------------
# Fast replacements for functions from Python's `random` module, backed by
# the C library's 48-bit linear congruential generators (drand48 / lrand48).
#
# The generator is seeded exactly once, at import time, from wall-clock time.
# NOTE: srand48 / drand48 / lrand48 are NOT thread-safe.
# -----------------------------------------------------------------------------
import time

cdef extern from "stdlib.h":
    void srand48(unsigned int sd)
    double drand48()
    unsigned long lrand48()

# Seed once at module init. Never re-seed per call (that destroys the
# sequence state) and never seed from clock() (CPU time, not wall time).
srand48(<unsigned int>time.time())


# -----------------------------------------------------------------------------
cdef inline unsigned long c_randbelow(unsigned long n):
    # Uniform random value in [0, n). Rejection sampling, like the stdlib's
    # random._randbelow: plain `lrand48() % n` is biased whenever n does not
    # divide 2**31 (by up to 2x for n in (2**30, 2**31]).
    cdef unsigned long limit
    if n > 0x7FFFFFFF:
        # Only reachable with absurd inputs (lists of 2**31+ elements);
        # plain modulo bias is negligible there
        return lrand48() % n
    limit = (0x7FFFFFFF // n) * n
    cdef unsigned long x = lrand48()
    while x >= limit:
        x = lrand48()
    return x % n
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef inline double random():
    """Return a random float in the range [0.0, 1.0).

    Replacement for: random.random()
    """
    return drand48()


cpdef inline list n_random(unsigned int n):
    """Return a list of n random floats in the range [0.0, 1.0).

    Replacement for: [random.random() for i in range(n)]
    """
    cdef unsigned int i
    return [drand48() for i in range(n)]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef inline int randint(int a, int b):
    """Return a random integer N such that a <= N <= b.

    Replacement for: random.randint()
    """
    if a > b:
        raise ValueError(f"empty range for randrange() ({a}, {b}, 1)")
    cdef unsigned long span = <unsigned long>b - <unsigned long>a + 1
    if span <= 0x7FFFFFFF:
        return a + <int>c_randbelow(span)
    # span > 2**31 (only possible with a < 0): combine two lrand48() draws
    # for 62 bits, then reject the biased tail the same way
    cdef unsigned long long limit = (0x3FFFFFFFFFFFFFFFULL // span) * span
    cdef unsigned long long x
    x = <unsigned long long>lrand48() * 0x80000000ULL + lrand48()
    while x >= limit:
        x = <unsigned long long>lrand48() * 0x80000000ULL + lrand48()
    return <int>(<long long>a + <long long>(x % span))


cpdef inline list n_randint(int a, int b, unsigned int n):
    """Return a list of n random integers in the range [a, b].

    Replacement for: [random.randint(a, b) for i in range(n)]
    """
    cdef unsigned int i
    return [randint(a, b) for i in range(n)]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef inline double uniform(double a, double b):
    """Return a random float in the range [a, b] (or [b, a] if a > b).

    Replacement for: random.uniform()
    """
    return a + (b - a) * drand48()


cpdef inline list n_uniform(double a, double b, unsigned int n):
    """Return a list of n random floats in the range [a, b].

    Replacement for: [random.uniform(a, b) for i in range(n)]
    """
    cdef unsigned int i
    return [uniform(a, b) for i in range(n)]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef inline object choice(list population):
    """Return a random element from a non-empty list.

    Replacement for: random.choice()
    """
    cdef unsigned int size = len(population)
    if size == 0:
        raise IndexError("Cannot choose from an empty sequence")
    return population[c_randbelow(size)]


# Note: the stdlib takes k as keyword-only, but cpdef does not support
# keyword-only arguments, so k is also accepted positionally here.
cpdef inline list choices(list population, unsigned int k=1):
    """Return a list of k random elements from a non-empty list.

    Replacement for: random.choices() (only the 'k' argument is supported)
    """
    cdef unsigned int size = len(population)
    if size == 0:
        raise IndexError("Cannot choose from an empty sequence")
    cdef unsigned int i
    return [population[c_randbelow(size)] for i in range(k)]
# -----------------------------------------------------------------------------
