import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import os
from EM1PythonFunctions import get_average, get_triple_product

chosen_subsection = "zerod"
variables = ["taue", "betan", "modeh", "qeff"]
# variables = ["taue", "q0", "q95", "qeff"]
start = 50
end = 100
save_graph = False
if save_graph:
    fig_file = input("Enter the name of the file to save the graph to: ")

base_path = "EM1 Data/8th Run Data (fast mode)"
file_name_template = "2023-02-03 NBI Ramping 0 to {last_pnbi_value}MW.mat"
last_pnbi_values = np.array(range(2, 11, 2))

files_paths = [
    os.path.join(base_path, file_name_template.format(last_pnbi_value=value))
    for value in last_pnbi_values
]


fig, axs = plt.subplots(1, len(variables) + 1, figsize=(15, 5))
plt.rcParams["figure.dpi"] = 150  # Sets the resolution of the figure (dots per inch)
plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = "\n".join(
    [
        r"\usepackage{siunitx}",
    ]
)
fig.suptitle(
    "Plots of the average values of the chosen variables against NBI power",
    fontsize=16,
)
axs[0].set_title("Triple Product")
axs[0].set_xlabel("NBI Power (MW)")
axs[0].set_ylabel("nTtaue")
for file_path, power in zip(files_paths, last_pnbi_values):
    results = get_triple_product(file_path, start, end)
    triple_product, avg, std = results
    axs[0].errorbar(power, avg, yerr=std, fmt=".", color="black", elinewidth=0.5)
for i, variable in enumerate(variables):
    axs[i + 1].set_title(f"{variable}")
    axs[i + 1].set_xlabel("NBI Power (MW)")
    axs[i + 1].set_ylabel(variable)
    for file_path, power in zip(files_paths, last_pnbi_values):
        # print(f"Getting data for {variable} at {power} MW")
        results = get_average(file_path, start, end, variables)
        variable, avg, std = results[i]
        # print("Average: ", avg, "Standard Deviation: ", std, "Variable: ", variable)
        # print(f"Plotting {variable} at {power} MW")
        axs[i + 1].errorbar(
            power, avg, yerr=std, fmt=".", color="black", elinewidth=0.5
        )
fig.tight_layout()
if save_graph:
    plt.savefig(fig_file, dpi=500)
plt.show()
