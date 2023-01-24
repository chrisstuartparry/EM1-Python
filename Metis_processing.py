import scipy.io
import numpy as np
import matplotlib.pyplot as plt

# load the data

chosen_subsection = "zerod"


def get_average(file_path, start, end, variables):
    full_dataset = scipy.io.loadmat(file_path)
    results = []
    for variable in variables:
        a = full_dataset["post"][chosen_subsection][0][0][variable][0][0]
        a = [float(x[0]) for x in a]
        avg = np.mean(a[start:end])
        std = np.std(a[start:end])
        results.append([variable, avg, std])
    return results


files_paths = [
    "EM1 Data/Second Run Data (standard mode)/2023-01-20 NBI Power 2MW.mat",
    "EM1 Data/Second Run Data (standard mode)/2023-01-20 NBI Power 4MW.mat",
    "EM1 Data/Second Run Data (standard mode)/2023-01-20 NBI Power 4MW.mat"
]

variables = ["te0", "ne0", "taue"]
start = 50
end = 100

for file_path in files_paths:
    results = get_average(file_path, start, end, variables)
    for variable, avg, std in results:
        print(
            f"Average for variable {variable} in {file_path} is: {avg} +/- {std} (std)"
        )
