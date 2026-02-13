# -----------------------------------------------------------------------------
# Import functions from stdlib.h C library
cdef extern from "stdlib.h":
    void srand48(unsigned int sd)
    unsigned long clock()
    double drand48()
    unsigned long lrand48()
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef inline double random():
# Returns a random float (double) between 0 and 1
# Replacement for random.random()
    return drand48()


cpdef inline list n_random(unsigned int n):
    # Returns a n-element list of random floats (double) between 0 and 1
    cdef unsigned int i
    return [drand48() for i in range(n)]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef inline int randint(int a, int b):
# Returns a random integer in range [a, b]
# Replacement for random.randint()
    return lrand48() % (b - a + 1) + a


cpdef inline list n_randint(int a, int b, unsigned int n):
    # Returns a n-element list of random integers in range [a, b]
    cdef unsigned int i
    return [randint(a, b) for i in range(n)]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef inline double uniform(double a, double b):
    # Returns a random float (double) between in range [a, b]
    # Replacement for random.uniform()
    return a + (b - a) * drand48()
    

cpdef inline list n_uniform(double a, double b, unsigned int n):
    # Returns a n-element list of random floats (double) in range [a, b]
    cdef unsigned int i
    return [uniform(a, b) for i in range(n)]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef inline choice(list population):
    # Returns a random element from a given list
    # Replacement for random.choice()
    cdef unsigned int size = len(population)
    return population[lrand48() % size]


cpdef inline list choices(list population, unsigned int k=1):
    # Given a list, returns a selection (list) of n random elements
    # Replacement for random.choices()
    cdef unsigned int i
    cdef unsigned int size = len(population)
    srand48(clock())
    return [population[lrand48() % size] for i in range(k)]
# -----------------------------------------------------------------------------
