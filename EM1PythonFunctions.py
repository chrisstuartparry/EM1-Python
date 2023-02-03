import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import os


def get_average(file_path, start, end, variables, chosen_subsection="zerod"):
    full_dataset = scipy.io.loadmat(file_path)
    results = []
    for variable in variables:
        a = full_dataset["post"][chosen_subsection][0][0][variable][0][0]
        a = [float(x[0]) for x in a]
        avg = np.mean(a[start:end])
        std = np.std(a[start:end])
        results.append([variable, avg, std])
    return results


def get_triple_product(file_path, start, end):
    full_dataset = scipy.io.loadmat(file_path)
    triple_product_variables = ["ni0", "tite", "taue"]
    results = []
    for variable in triple_product_variables:
        a = full_dataset["post"]["zerod"][0][0][variable][0][0]
        a = [float(x[0]) for x in a]
        avg = np.mean(a[start:end])
        std = np.std(a[start:end])
        results.append([variable, avg, std])
    triple_product_avg = results[0][1] * results[1][1] * results[2][1]
    triple_product_std = triple_product_avg * np.sqrt(
        (results[0][2] / results[0][1]) ** 2
        + (results[1][2] / results[1][1]) ** 2
        + (results[2][2] / results[2][1]) ** 2
    )
    return ["triple_product", triple_product_avg, triple_product_std]
