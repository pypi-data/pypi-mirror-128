# Markovian Bandits

This repository contains a python library to compute whittle or indices for finite-state Markovian bandit problems. 

## Installation 

To install, just run: 
```
pip install markovianbandit-pkg
```

## Example

To test with a few randomly generated examples: 
```
import markovianbandit.markovianbandit as bandit
model = bandit.random_restless(dim=4, seed=42)
print(model.whittle_indices()) # should print (True, array([ 0.87536099, -0.08765819, -0.15279431, -0.51905682]))
print(model.get_P0P1R0R1())
model = bandit.random_restless(4, seed=2791)
print(model.is_indexable()) # should print False

model = bandit.random_rested(dim=4)
print(model.gittins_indices(discount=.8)) # computes gittins index
```

To compute the Whittle or Gittins index from P0 and P1: 
```
P0 = [[.5, .5], [.25, .75]]
P1 = [[1, 0], [0.5, 0.5]]
R0 = [0.5, 0.5]
R1 = [2, 1]
model = bandit.restless_bandit_from_P0P1_R0R1(P0, P1, R0, R1)
print(model.whittle_indices())

model = bandit.rested_bandit_from_P1_R1(P1, R1)
print(model.gittins_indices(discount=0.5))
```

Note that the algorithm complexity to compute Whittle index is $O(n^3)$. It can compute indices of bandits in less than one seconds to bandits of up to $1000$ states (i.e. $1000\times 1000$ matrices). The loop below should take less than one second.
```
import time
for dim in [10, 100, 1000]:
    ts = time.time()
    model = bandit.random_restless(dim=dim, seed=42)
    model.whittle_indices()
    print("Model of size", dim, "computed in", time.time() - ts, "seconds")
```

## Reference


