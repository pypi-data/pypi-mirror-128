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
model = bandit.random_restless(dim=4)
print(model.whittle_indices()) # should print (True, array([ 0.51679937, -0.09224213,  0.32943948,  0.29512467]))

model = bandit.random_restless(4, seed=2791)
print(model.is_indexable()) # should print False

model = bandit.random_rested(dim=4)
print(model.gittins_indices(discount=.8)) # computes gittins index

```

## Reference


