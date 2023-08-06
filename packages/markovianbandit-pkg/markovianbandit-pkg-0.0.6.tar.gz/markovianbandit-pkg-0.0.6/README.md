# Markovian Bandits

This repository contains a python library to compute whittle or indices for finite-state Markovian bandit problems. 

## Installation 

To install, just run: 
```
pip install markovianbandit-pkg
```

## Example

```
from markovianbandit import markovianbandit as bandit
model = bandit.random_restless(dim=4, seed=42)
print(model.whittle_indices()) # should print (True, array([ 0.87536099, -0.08765819, -0.15279431, -0.51905682]))
print(model.get_P0P1R0R1())
model = bandit.random_restless(4, seed=2791)
print(model.is_indexable()) # should print False

model = bandit.random_rested(dim=4)
print(model.gittins_indices(discount=.8)) # computes gittins index

# to construct an example from probability matrices
P0 = [[.5, .5], [.25, .75]]
P1 = [[1, 0], [0.5, 0.5]]
R0 = [0.5, 0.5]
R1 = [1, 2]
model = bandit.RestlessBandit.from_P0_P1_R0_R1(P0, P1, R0, R1)
print(model.whittle_indices())
```

## Reference


