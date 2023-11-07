import random as rand

rules = {
    "Only mons starting with x": True,
    "Only moves starting with x": True
}

choice = rand.choice(list(rules.items()))
