import numpy as np

def power(a, b):
    return a ** b

def mean(lst):
    num_list = np.zeros(len(lst))
    num_list[:] = lst
    return np.mean(num_list)
