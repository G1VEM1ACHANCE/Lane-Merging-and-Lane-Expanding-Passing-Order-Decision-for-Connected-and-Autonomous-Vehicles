import math
import random

def nextTime(rateParameter):
    return random.expovariate(rateParameter)
print(nextTime(0.6))