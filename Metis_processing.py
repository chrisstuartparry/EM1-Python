#!/usr/bin/env python3

import scipy.io
from matplotlib import pyplot as plt
import numpy as np

# load the data
full_dataset = scipy.io.loadmat("EM1 Data/Second Run Data (standard mode)/2023-01-20 NBI Power 2MW.mat", variable_names=['post'])


def list_subsections():
    print("subsections (I'm using zerod by default):")
    print(full_dataset['post'].dtype)


def list_indexes(subsection='zerod'):
    print("indexes in subsection " + subsection + ":")
    print(full_dataset['post']['zerod'][0][0].dtype)


def get_variable(index, subsection='zerod'):
    a = full_dataset['post'][subsection][0][0][index][0][0]
    a = [float(x[0]) for x in a]
    return a

def get_average(start, end, index, subsection='zerod'):
    a = get_variable(index, subsection=subsection)
    print("DEBUG: getting average for index", index, "from", start, "to", end)
    print("DEBUG: raw data is:", a)
    return (np.mean(a[start:end]), np.std(a[start:end]))


list_subsections()
list_indexes()
print(get_average(50, 100, 'te0'))
plt.plot(get_variable('te0'))
plt.show()
