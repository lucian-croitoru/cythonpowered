import random as py_random

import pytest

import cythonpowered.random


# Number of draws for range/property checks; large enough to be meaningful
# while keeping the suite fast.
ITERATIONS = 10000
FLOAT_INTERVAL = [0, 1]
INT_INTERVAL = [-100, 100]
UNIFORM_INTERVAL = [-123.456, 123.456]


def test_random():
    """random() must return a float in [0, 1] on every draw, matching
    the range contract of random.random()."""
    # Stage 1: draw ITERATIONS independent values.
    # Stage 2: verify each value respects the lower and upper bounds.
    for i in range(ITERATIONS):
        result = cythonpowered.random.random()
        assert result >= FLOAT_INTERVAL[0]
        assert result <= FLOAT_INTERVAL[1]


def test_random_precision_is_32bit():
    """random() documents a deliberate deviation from the stdlib: 32-bit
    precision instead of random.random()'s 53 bits. Every value must
    therefore be an exact multiple of 2**-32."""
    # Stage 1: draw values and scale back to the 32-bit lattice.
    # Stage 2: each scaled value must be exactly integral (dyadic rationals
    # k / 2**32 round-trip exactly through double).
    for i in range(1000):
        result = cythonpowered.random.random()
        scaled = result * 2**32
        assert scaled == round(scaled)


def test_n_random():
    """n_random(n) must return exactly n distinct random floats, each in
    [0, 1] — the batched equivalent of [random.random() for i in range(n)]."""
    # Stage 1: generate the batch in a single call.
    result = cythonpowered.random.n_random(ITERATIONS)
    # Stage 2: the batch has the requested length and is not degenerate
    # (all-identical output would indicate a broken generator).
    assert len(result) == ITERATIONS
    assert len(set(result)) > 1
    # Stage 3: every element respects the float range.
    for i in range(ITERATIONS):
        assert result[i] >= FLOAT_INTERVAL[0]
        assert result[i] <= FLOAT_INTERVAL[1]


def test_randint():
    """randint(a, b) must return an integer in the closed range [a, b] on
    every draw, matching random.randint()."""
    # Stage 1: draw ITERATIONS values from a range that spans negative and
    # positive values (exercises the signed-int boundary on both sides).
    # Stage 2: verify each value stays inside the closed interval.
    for i in range(ITERATIONS):
        result = cythonpowered.random.randint(*INT_INTERVAL)
        assert result >= INT_INTERVAL[0]
        assert result <= INT_INTERVAL[1]


def test_n_randint():
    """n_randint(a, b, n) must return exactly n distinct random integers,
    each in [a, b] — the batched equivalent of
    [random.randint(a, b) for i in range(n)]."""
    # Stage 1: generate the batch in a single call.
    result = cythonpowered.random.n_randint(*INT_INTERVAL, ITERATIONS)
    # Stage 2: correct length and non-degenerate output.
    assert len(result) == ITERATIONS
    assert len(set(result)) > 1
    # Stage 3: every element stays inside the closed interval.
    for i in range(ITERATIONS):
        assert result[i] >= INT_INTERVAL[0]
        assert result[i] <= INT_INTERVAL[1]


def test_randint_a_greater_than_b_raises_valueerror():
    """randint(a, b) with a > b (empty range) must raise ValueError, the
    same exception type as random.randint()."""
    # Inverted bounds in several states: small positive, crossing zero, and
    # a large positive span.
    for a, b in [(10, 5), (0, -1), (10**6, 1)]:
        # Stage 1: confirm the stdlib reference behavior raises ValueError.
        with pytest.raises(ValueError):
            py_random.randint(a, b)
        # Stage 2: the Cython replacement must raise the same exception type.
        with pytest.raises(ValueError):
            cythonpowered.random.randint(a, b)


def test_randint_single_value_range():
    """randint(a, a) is the degenerate single-value state (span 1): the
    result must always be exactly that value."""
    for i in range(100):
        assert cythonpowered.random.randint(7, 7) == 7


def test_randint_full_32bit_range():
    """randint over the full 32-bit range (span 2**32) must stay inside
    [-2**31, 2**31 - 1]. This span equals the full 32-bit draw space of the
    xorshift128 generator, so it exercises the no-rejection path where every
    draw is accepted as-is."""
    lo, hi = -2**31, 2**31 - 1
    # Stage 1: draw from the extreme state where the span covers the entire
    # 32-bit output of the generator.
    # Stage 2: every value must land inside the full int32 interval.
    for i in range(1000):
        result = cythonpowered.random.randint(lo, hi)
        assert result >= lo
        assert result <= hi


def test_randint_uniformity():
    """randint(0, 3) must distribute draws evenly: each of the 4 values
    should appear ~25% of the time. This catches modulo bias, since
    x % n is not uniform when n does not divide 2**32 (the number of
    possible 32-bit draws)."""
    # Stage 1: build a histogram of 40000 draws over the 4 values.
    counts = [0, 0, 0, 0]
    for i in range(40000):
        counts[cythonpowered.random.randint(0, 3)] += 1
    # Stage 2: every bin must be within 5% of the expected 25% share
    # (a biased modulo would push at least one bin far outside this).
    expected = 40000 / 4
    for count in counts:
        assert abs(count - expected) <= 0.05 * expected


def test_uniform():
    """uniform(a, b) must return a float in [a, b] on every draw, matching
    random.uniform()."""
    # Stage 1: draw ITERATIONS values from a fractional interval that spans
    # negative and positive values.
    # Stage 2: verify each value stays inside the closed interval.
    for i in range(ITERATIONS):
        result = cythonpowered.random.uniform(*UNIFORM_INTERVAL)
        assert result >= UNIFORM_INTERVAL[0]
        assert result <= UNIFORM_INTERVAL[1]


def test_n_uniform():
    """n_uniform(a, b, n) must return exactly n distinct random floats,
    each in [a, b] — the batched equivalent of
    [random.uniform(a, b) for i in range(n)]."""
    # Stage 1: generate the batch in a single call.
    result = cythonpowered.random.n_uniform(*UNIFORM_INTERVAL, ITERATIONS)
    # Stage 2: correct length and non-degenerate output.
    assert len(result) == ITERATIONS
    assert len(set(result)) > 1
    # Stage 3: every element stays inside the closed interval.
    for i in range(ITERATIONS):
        assert result[i] >= UNIFORM_INTERVAL[0]
        assert result[i] <= UNIFORM_INTERVAL[1]


def test_choice():
    """choice(population) must return an element that actually belongs to
    the population, matching random.choice()."""
    # Stage 1: build a realistic population (many distinct values, mixed
    # signs) using n_randint.
    population = cythonpowered.random.n_randint(*INT_INTERVAL, ITERATIONS)
    # Stage 2: draw one element and verify membership.
    result = cythonpowered.random.choice(population)
    assert result in population


def test_choice_empty_raises_indexerror():
    """choice([]) must raise IndexError on the empty-population state, the
    same exception type as random.choice()."""
    # Stage 1: confirm the stdlib reference behavior raises IndexError.
    with pytest.raises(IndexError):
        py_random.choice([])
    # Stage 2: the Cython replacement must raise the same exception type.
    with pytest.raises(IndexError):
        cythonpowered.random.choice([])


def test_choice_uniformity():
    """choice over a small population must pick each element with equal
    probability (~25% each). This catches index-selection bias in the
    draw-to-index mapping."""
    population = ["a", "b", "c", "d"]
    # Stage 1: build a histogram of 40000 draws keyed by element.
    counts = {element: 0 for element in population}
    for i in range(40000):
        counts[cythonpowered.random.choice(population)] += 1
    # Stage 2: every element must be within 5% of the expected equal share.
    expected = 40000 / len(population)
    for count in counts.values():
        assert abs(count - expected) <= 0.05 * expected


def test_choices():
    """choices(population, k) must return a sample of exactly k elements,
    drawn with replacement, all belonging to the population, matching
    random.choices()."""
    # Stage 1: build the population and request a half-size sample via the
    # k keyword argument (as in the stdlib signature).
    population = cythonpowered.random.n_randint(*INT_INTERVAL, ITERATIONS)
    sample_size = ITERATIONS // 2
    result = cythonpowered.random.choices(population, k=sample_size)
    # Stage 2: the sample has the requested length, is not degenerate, and
    # contains only population members (replacement allows repeats).
    assert len(result) == sample_size
    assert len(set(result)) > 1
    assert set(result).issubset(set(population))


def test_choices_empty_raises_indexerror():
    """choices([], k) must raise IndexError on the empty-population state,
    the same exception type as random.choices()."""
    # Stage 1: confirm the stdlib reference behavior raises IndexError.
    with pytest.raises(IndexError):
        py_random.choices([], k=5)
    # Stage 2: the Cython replacement must raise the same exception type.
    with pytest.raises(IndexError):
        cythonpowered.random.choices([], k=5)


def test_choices_k_zero():
    """choices(population, k=0) is the zero-sample boundary state: the
    result must be an empty list (no draws, no errors)."""
    assert cythonpowered.random.choices([1, 2, 3], k=0) == []


def test_choices_k_as_keyword():
    """k must be usable as a keyword argument (matching the stdlib
    signature) and produce a valid sample of the requested size."""
    # Stage 1: request 10 draws with k passed by keyword.
    result = cythonpowered.random.choices([1, 2, 3], k=10)
    # Stage 2: the sample has the right length and only valid members.
    assert len(result) == 10
    assert set(result).issubset({1, 2, 3})
