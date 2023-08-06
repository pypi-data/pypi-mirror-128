


import os



import numpy as np


def min_fast(a, b):
    '''
    1.5 times faster than row min(a, b)
    '''
    return  a if a < b else b

def max_fast(a, b):
    return a if a > b else b


def folder_create(folder: str):
    if not os.path.exists(folder):
        os.makedirs(folder)


def can_be_prob(value):
    return value >=0 and value <=1


def is_numpy(arg):
    return type(arg) == np.ndarray