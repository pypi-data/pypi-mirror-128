# Chainrand-py — Verifiable hybrid-chain RNG.

Many applications require off-chain generation of random numbers for efficiency, security, etc.

This class allows you to generate a stream of deterministic, high-quality,  
cryptographically secure random numbers.

By seeding it with a Chainlink VRF result that is requested **only once for the project**,  
it can be used to demonstrate that the random numbers are **not cherry-picked**.

# Installation

**PIP:**

```bash
pip install chainrand
```

Or you can clone/download this GitHub repository.  

```bash
git clone https://github.com/chainrand/chainrand-py
cd chainrand-py
python setup.py install
```

## Usage

```python
rng = chainrand.CRNG("base10(<RNG_VRF_RESULT>)" + "<RNG_SEED_KEY>")
// prints 10 determinstic random numbers between [0, 1)
for i in range(10):
    print(rng())
```

# Reproducibility

Current and future versions of this library will generate the same stream of random numbers from the same seed.

# Functions

## Constructor

```python
chainrand.CRNG(seed)
```

Creates an instance of the crng initialized with the `seed`.

**Parameters:**

- `seed: str` If empty, defaults to the empty string `""`.

**Example:**

```python
crng = chainrand.CRNG("base10(<RNG_VRF_RESULT>)" + "<RNG_SEED_KEY>")
```

## random

```python
crng.random(): float
```

Alias for `crng()`.
Returns a random number uniformly distributed in [0, 1).  
The numbers are in multiples of `2**-53`.

**Parameters:**
none

**Returns:**
A random number uniformly distributed in [0, 1).

## randrange

```python
crng.randrange(start, stop[, step]): float
crng.randrange(stop): float
```

Returns a random integer uniformly distributed in [start, stop).  
The integers are spaced with intervals of |step|.

**Parameters:**

- `start: int` The start of the range. (optional, default=`0`)
- `stop: int` The end of the range.
- `step: int` The interval step. (optional, default=`1`)

**Returns:**

A random integer uniformly distributed in [start, stop).

**Examples:**

```python
r = crng.randrange(3) # returns a random number in {0,1,2}
r = crng.randrange(-3) # returns a random number in {0,-1,-2}
r = crng.randrange(0, 6, 2) # returns a random number in {0,2,4}
r = crng.randrange(5, 0, 1) # returns a random number in {5,4,3,2,1}
r = crng.randrange(5, -5, -2) # returns a random number in {5,3,1,-1,-3}
```

## randint

```python
crng.randint(start, stop): int
crng.randint(stop): int
```

Returns a random integer uniformly distributed in [start, stop].  
The integers are spaced with intervals of |step|.

**Parameters:**

- `start: int` The start of the range. (optional, default=`0`)
- `stop: int` The end of the range.

**Returns:**

A random integer uniformly distributed in [start, stop].

**Examples:**

```python
r = crng.randint(3) # returns a random number in {0,1,2,3}
r = crng.randint(-3) # returns a random number in {0,-1,-2,-3}
r = crng.randint(-3, 1) # returns a random number in {-3,-2,-1,0,1}
r = crng.randint(3, -1) # returns a random number in {3,2,1,0,-1}
```

## choice

```python
crng.choice(population[, weights]): list
```

Returns a random element from the population.

If weights is not provided, every element of population will be equally weighted.

If weights is a non-empty array and is of different length to population,  
only the first `Math.min(population.length, weights.length)` elements of population are sampled.

If the sum of the weights is less than or equal to zero,  
every element of population will be equally weighted.

**Parameters:**

- `population: list`  The population.
- `weights: list<float>` The weights of the population. (optional)

**Returns:**

A random element in the population.

**Examples:**

```python
# returns a random number in {1,2,3} 
r = crng.choice([1,2,3]) 

# returns a random number in {1,2,3}
# with the weights {1:10, 2:1, 3:0.1} 
r = crng.choice([1,2,3], [10,1,0.1]) 
```

## sample

```python
crng.sample(population, k=1[, weights]): list
```

Returns `k` random elements from the population, sampling **without** replacement.

If `k` is more than the length of the population, only `k` elements will be returned.

If weights is not provided, every element of population will be equally weighted.

If weights is a non-empty array and is of different length to population,  
only the first `Math.min(population.length, weights.length)` elements of population are sampled.

If the sum of the weights is less than or equal to zero,  
every element of population will be equally weighted.

**Parameters:**

- `population: list`  The population.
- `k: int` The number of elements to choose.
- `weights: list<float>` The weights of the population. (optional)

**Returns:**

An array of `k` random elements from the population.

**Examples:**

```python
# returns an array of 1 random element from {1,2,3}
r = crng.sample([1,2,3]) 

# returns an array of 2 random elements from {1,2,3}
r = crng.sample([1,2,3], 2) 

# returns an array of 2 random elements from {1,2,3}
# with the weights {1:10, 2:1, 3:0.1} 
r = crng.sample([1,2,3], 2, [10,1,0.1]) 
```

## shuffle

```python
crng.shuffle(population)
```

Shuffles the array in-place.

**Parameters:**

- `population: list`  The population.

**Returns:** 

The shuffled array. 

## gauss

```python
crng.gauss(mu=0.0, sigma=1.0): float
```

Normal distribution, also called the Gaussian distribution. 

**Parameters:**

- `mu: float`  The mean. (optional, default=`0.0`)
- `sigma: float` The standard deviation. (optional, default=`1.0`)

**Returns:**

A random number from the Gaussian distribution.

# License

MIT
