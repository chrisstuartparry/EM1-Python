import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import os

def division(a, b):
    return a / b if a % b else a // b
print(division(5,2))
print(division(10,2))

base_path = "EM1 Data/4th Run Data (fast mode)"
file_name_template = "2023-01-27 NBI Power 2MW B0 {B0_value}T.mat"
B0_values = np.array(range(1,41,1), dtype=float)
for i in range(len(B0_values)):
    B0_values[i] = division(B0_values[i],10)
    
print(f"B0_values: {B0_values}")

def get_triple_product(file_path, start, end):
    full_dataset = scipy.io.loadmat(file_path)
    triple_product_variables = ["ne0", "te0", "taue"]
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