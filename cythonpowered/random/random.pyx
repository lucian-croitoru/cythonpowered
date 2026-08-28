# -----------------------------------------------------------------------------
# Fast replacements for functions from Python's `random` module.
#
# PRNG: xorshift128 (Marsaglia, 2003) — 128-bit state, period 2**128 - 1,
# 32-bit output, no multiplication in the core step. Chosen over the C
# library's 48-bit LCG (srand48/drand48/lrand48) for better statistical
# quality and a cheaper inlined core step.
#
# The 128-bit state is module-global mutable state (see _x0.._x3 below).
# It is seeded exactly once at import time from wall-clock time, expanded
# via splitmix64. NOTE: the generator is NOT thread-safe.
# -----------------------------------------------------------------------------
import time


# -----------------------------------------------------------------------------
# xorshift128 state (Marsaglia, 2003). Must never be all zero: the all-zero
# state is a fixed point and would emit zeros forever.
cdef unsigned int _x0
cdef unsigned int _x1
cdef unsigned int _x2
cdef unsigned int _x3

# splitmix64 state, used only at import to expand the 32-bit wall-clock seed
# into 128 bits of xorshift128 state.
cdef unsigned long long _seed_state

# Largest span a single 32-bit draw can cover (2**32). Typed so that
# span comparisons stay at C level — a bare 0x100000000 literal makes
# Cython emit a Python-object comparison (with an allocation) per call.
cdef unsigned long long MAX_SPAN = 0x100000000


cdef inline unsigned long long c_splitmix64():
    # Expands a 64-bit counter into well-mixed 64-bit outputs (seeding only,
    # not part of the hot path).
    global _seed_state
    _seed_state += 0x9E3779B97F4A7C15ULL  # 64-bit golden-ratio constant 
    cdef unsigned long long z = _seed_state
    # These are the two mixing multipliers of splitmix64
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL
    return z ^ (z >> 31)


cdef inline unsigned int c_xorshift128():
    # One xorshift128 step: 3 shifts + 3 XORs, no multiplication.
    global _x0, _x1, _x2, _x3
    cdef unsigned int t = _x0 ^ (_x0 << 11)
    _x0 = _x1
    _x1 = _x2
    _x2 = _x3
    _x3 = _x3 ^ (_x3 >> 19) ^ t ^ (t >> 8)
    return _x3


# Seed once at module init. Never re-seed per call (that destroys the
# sequence state) and never seed from clock() (CPU time, not wall time).
_seed_state = <unsigned long long>time.time()
_x0 = <unsigned int>c_splitmix64()
_x1 = <unsigned int>(c_splitmix64() >> 32)
_x2 = <unsigned int>c_splitmix64()
_x3 = <unsigned int>(c_splitmix64() >> 32)
if _x0 == 0 and _x1 == 0 and _x2 == 0 and _x3 == 0:
    _x0 = 1
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline double c_random():
    # 32-bit draw scaled to [0.0, 1.0); 32-bit mantissa precision
    # (the stdlib's random.random() offers 53 bits).
    return <double>c_xorshift128() / 4294967296.0  # (2**32)


cdef inline unsigned int c_randbelow(unsigned int n):
    # Uniform random value in [0, n) for n in [1, 2**32). Rejection
    # sampling, like the stdlib's random._randbelow: plain `x % n` is
    # biased whenever n does not divide 2**32 (the number of possible
    # 32-bit draws).
    return c_randbelow_limit(n, (MAX_SPAN // n) * n)


cdef inline unsigned int c_randbelow_limit(unsigned int n, unsigned long long limit):
    # Rejection-sampling core with a precomputed limit, so batched callers
    # can compute the (expensive) 64-bit division once per span instead of
    # once per draw.
    cdef unsigned int x = c_xorshift128()
    while <unsigned long long>x >= limit:
        x = c_xorshift128()
    return x % n
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef inline double random():
    """Return a random float in the range [0.0, 1.0).

    32-bit precision (the stdlib's random.random() offers 53 bits).
    Replacement for: random.random()
    """
    return c_random()


cpdef inline list n_random(unsigned int n):
    """Return a list of n random floats in the range [0.0, 1.0).

    Replacement for: [random.random() for i in range(n)]
    """
    cdef unsigned int i
    return [c_random() for i in range(n)]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef inline int randint(int a, int b):
    """Return a random integer N such that a <= N <= b.

    Replacement for: random.randint()
    """
    if a > b:
        raise ValueError(f"empty range for randrange() ({a}, {b}, 1)")
    cdef unsigned long span = <unsigned long>b - <unsigned long>a + 1
    if span < MAX_SPAN:
        # span fits in a single 32-bit draw (1..2**32 - 1)
        return <int>(<long long>a + <long long>c_randbelow(<unsigned int>span))
    # span == 2**32 (only a = -2**31, b = 2**31 - 1): every 32-bit draw is
    # in range, so no rejection or modulo is needed
    return <int>(<long long>a + <long long>c_xorshift128())


cpdef inline list n_randint(int a, int b, unsigned int n):
    """Return a list of n random integers in the range [a, b].

    Replacement for: [random.randint(a, b) for i in range(n)]
    """
    if a > b:
        raise ValueError(f"empty range for randrange() ({a}, {b}, 1)")
    cdef unsigned long span = <unsigned long>b - <unsigned long>a + 1
    cdef unsigned long long limit
    cdef unsigned int i
    if span < MAX_SPAN:
        # span fits in a single 32-bit draw (1..2**32 - 1); the rejection
        # limit depends only on span, so it is computed once, not per draw
        limit = (MAX_SPAN // span) * span
        return [<int>(<long long>a + <long long>c_randbelow_limit(<unsigned int>span, limit)) for i in range(n)]
    # span == 2**32 (only a = -2**31, b = 2**31 - 1): every 32-bit draw is
    # in range, so no rejection or modulo is needed
    return [<int>(<long long>a + <long long>c_xorshift128()) for i in range(n)]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef inline double uniform(double a, double b):
    """Return a random float in the range [a, b] (or [b, a] if a > b).

    Replacement for: random.uniform()
    """
    return a + (b - a) * c_random()


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
