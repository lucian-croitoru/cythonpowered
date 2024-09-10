import cythonpowered.random


ITERATIONS = 10000
FLOAT_INTERVAL = [0, 1]
INT_INTERVAL = [-100, 100]
UNIFORM_INTERVAL = [-123.456, 123.456]


def test_random():
    for i in range(ITERATIONS):
        result = cythonpowered.random.random()
        assert result >= FLOAT_INTERVAL[0]
        assert result <= FLOAT_INTERVAL[1]


def test_n_random():
    result = cythonpowered.random.n_random(ITERATIONS)
    assert len(result) == ITERATIONS
    assert len(set(result)) > 1

    for i in range(ITERATIONS):
        assert result[i] >= FLOAT_INTERVAL[0]
        assert result[i] <= FLOAT_INTERVAL[1]


def test_randint():
    for i in range(ITERATIONS):
        result = cythonpowered.random.randint(*INT_INTERVAL)
        assert result >= INT_INTERVAL[0]
        assert result <= INT_INTERVAL[1]


def test_n_randint():
    result = cythonpowered.random.n_randint(*INT_INTERVAL, ITERATIONS)
    assert len(result) == ITERATIONS
    assert len(set(result)) > 1

    for i in range(ITERATIONS):
        assert result[i] >= INT_INTERVAL[0]
        assert result[i] <= INT_INTERVAL[1]


def test_uniform():
    for i in range(ITERATIONS):
        result = cythonpowered.random.uniform(*UNIFORM_INTERVAL)
        assert result >= UNIFORM_INTERVAL[0]
        assert result <= UNIFORM_INTERVAL[1]


def test_n_uniform():
    result = cythonpowered.random.n_uniform(*UNIFORM_INTERVAL, ITERATIONS)
    assert len(result) == ITERATIONS
    assert len(set(result)) > 1

    for i in range(ITERATIONS):
        assert result[i] >= UNIFORM_INTERVAL[0]
        assert result[i] <= UNIFORM_INTERVAL[1]


def test_choice():
    population = cythonpowered.random.n_randint(*INT_INTERVAL, ITERATIONS)
    result = cythonpowered.random.choice(population)
    assert result in population


def test_choices():
    population = cythonpowered.random.n_randint(*INT_INTERVAL, ITERATIONS)
    sample_size = ITERATIONS // 2
    result = cythonpowered.random.choices(population, sample_size)

    assert len(result) == sample_size
    assert len(set(result)) > 1
    assert set(result).issubset(set(population))
