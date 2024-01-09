import math
from random import Random

def random_bm(mu, sigma):
    u = 0
    v = 0
    while(u == 0): 
        u = random()
    while(v == 0): 
        v = random()
    mag = sigma * math.sqrt( -2.0 * math.log( u ) )
    return mag * math.cos( 2.0 * math.pi * v ) + mu

def calcImpLoss(lowerLimit, upperLimit, px):
    r = math.sqrt(upperLimit/lowerLimit)
    a1 = (math.sqrt(r) - px)
    a2 = (math.sqrt(r) / (math.sqrt(r) - 1)) * (2*math.sqrt(px) - (px + 1))
    a3 = (math.sqrt(r) * px - 1)
    if(px < 1/r):
        return a3
    elif(px > r): 
        return a1
    
    return a2;

def calcExpImpLoss(rangePerc, mu, sigma) :
    upperPx = 1 + rangePerc
    lowerPx = 1 / upperPx
    Vhsum = 0
    impLossSum = 0
    iterations = 10000
    for i in range(iterations) :
        t = 1
        W = random_bm(0, 1) * math.sqrt(t-0)
        X = (math.log(1 + mu) - 0.5 * math.pow(math.log(1 + sigma), 2)) * t + math.log(1 + sigma) * W
        _px = math.exp(X)
        Vhsum += 1 + _px
        impLossSum += calcImpLoss(lowerPx, upperPx, _px)
    
    return (impLossSum/iterations)/(Vhsum/iterations)

