import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import os


base_path = "EM1 Data/4th Run Data (fast mode)"
file_name_template = "2023-01-27 NBI Power 2MW B0 {B0_value}T.mat"
B0_values = np.array(range(1,41,1), dtype=float)/10

files_paths = [
    os.path.join(base_path, file_name_template.format(B0_value=value))
    for value in B0_values
]

start = 50
end = 100

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


fig, axs = plt.subplots(1, 1, figsize=(18, 6))
plt.rcParams["figure.dpi"] = 150  # Sets the resolution of the figure (dots per inch)
plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = "\n".join(
    [
        r"\usepackage{siunitx}",
    ]
)
axs.set_title("Triple Product")
axs.set_xlabel("Power (MW)")
axs.set_ylabel("nTtaue")
for file_path, power in zip(files_paths, B0_values):
    results = get_triple_product(file_path, start, end)
    triple_product, avg, std = results
    axs.errorbar(power, avg, yerr=std, fmt=".", color="black", elinewidth=0.5)
fig.tight_layout()
plt.show()