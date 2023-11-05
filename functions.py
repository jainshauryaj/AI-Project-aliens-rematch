import numpy as np

def bayesian_update(probs, beep, alpha, distances):
    if beep:
        likelihood = np.exp(-alpha * (distances - 1))
    else:
        likelihood = 1 - np.exp(-alpha * (distances - 1))
    updated_probs = probs * likelihood
    return updated_probs / updated_probs.sum()
