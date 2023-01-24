#!/usr/bin/env python3

import scipy.io
from matplotlib import pyplot as plt
import numpy as np
import csv

# load the data
full_dataset = scipy.io.loadmat(
    "EM1 Data/Second Run Data (standard mode)/2023-01-20 NBI Power 2MW.mat"
)


def list_subsections():
    print("subsections:")
    print(full_dataset["post"].dtype)


chosen_subsection = "zerod"
chosen_index = "te0"


def list_indexes(subsection):
    print("indexes in subsection " + subsection + ":")
    print(full_dataset["post"][chosen_subsection][0][0].dtype)


def get_variable(index, subsection):
    a = full_dataset["post"][subsection][0][0][index][0][0]
    a = [float(x[0]) for x in a]
    return a


def get_average(start, end, index, subsection):
    a = get_variable(index, subsection=subsection)
    print("DEBUG: getting average for variable", index, "from", start, "to", end)
    # print("DEBUG: raw data is:", a)
    return (np.mean(a[start:end]), np.std(a[start:end]), index)


# list_subsections()
# list_indexes()
# print(get_average(50, 100, 'te0'))
# plt.plot(get_variable('te0'))
# plt.show()

print(
    "Average for variable ",
    get_average(50, 100, chosen_index, chosen_subsection)[2],
    " is: ",
    get_average(50, 100, chosen_index, chosen_subsection)[0],
    " +/- ",
    get_average(50, 100, chosen_index, chosen_subsection)[1],
    " (std)",
)

result = get_average(50, 100, chosen_index, chosen_subsection)

# open a csv file to write the results

with open("results.csv", mode="w", newline="") as results_file:
    results_writer = csv.writer(
        results_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    # write the header row
    results_writer.writerow(["Variable", "Average", "STD"])
    # write the results
    results_writer.writerow([result[2], result[0], result[1]])

print("Results written to results.csv.")
