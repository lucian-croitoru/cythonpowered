# -----------------------------------------------------------------------------
# Import functions from stdlib.h C library
cdef extern from "stdlib.h":
    void srand(unsigned int sd)
    unsigned int rand()
    unsigned long clock()
    double drand48()
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef double random():
# Returns a random float (double) between 0 and 1
# Replacement for random.random()
    return drand48()


cpdef list n_random(unsigned int n):
    # Returns a n-element list of random floats (double) between 0 and 1
    cdef unsigned int i
    return [drand48() for i in range(n)]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef int randint(int a, int b):
# Returns a random integer in range [a, b]
# Replacement for random.randint()
    return rand() % (b - a + 1) + a


cpdef list n_randint(int a, int b, unsigned int n):
    # Returns a n-element list of random integers in range [a, b]
    cdef unsigned int i
    return [randint(a, b) for i in range(n)]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef double uniform(double a, double b):
    # Returns a random float (double) between in range [a, b]
    # Replacement for random.uniform()
    return a + (b - a) * drand48()
    

cpdef list n_uniform(double a, double b, unsigned int n):
    # Returns a n-element list of random floats (double) in range [a, b]
    cdef unsigned int i
    return [uniform(a, b) for i in range(n)]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef choice(list population):
    # Returns a random element from a given list
    # Replacement for random.choice()
    cdef unsigned int size = len(population)
    return population[rand() % size]


cpdef list choices(list population, unsigned int n):
    # Given a list, returns a selection (list) of n random elements
    # Replacement for random.choices()
    cdef unsigned int i
    cdef unsigned int size = len(population)
    srand(clock())
    return [population[rand() % size] for i in range(n)]
# -----------------------------------------------------------------------------
