import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import os
from EM1PythonFunctions import get_average, get_triple_product, get_variable

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
file_values = np.array(range(2, 11, 2))

files_paths = [
    os.path.join(base_path, file_name_template.format(last_pnbi_value=value))
    for value in file_values
]


nrows = len(files_paths)
ncols = len(variables)
fig, axs = plt.subplots(nrows, ncols, figsize=(15, 5 * nrows), constrained_layout=True)
plt.rcParams["figure.dpi"] = 150  # Sets the resolution of the figure (dots per inch)
plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = "\n".join(
    [
        r"\usepackage{siunitx}",
    ]
)
fig.suptitle(
    "Plots of the chosen variables against Time (s)",
    fontsize=16,
)


def plot_variable(files_paths, file_values, variables, axs):
    for i, file_path in enumerate(files_paths):
        for j, variable in enumerate(variables):
            ax = axs[i, j]
            if i == 0:
                ax.set_title(f"{variable}")
            time_results = get_variable(file_path, ["temps"])
            times = time_results[0][1]
            results = get_variable(file_path, variables)
            variable, ydata = results[j]
            ax.plot(times, ydata, ".", color="black")
            if i == nrows - 1:
                ax.set_xlabel("Time (s)")
            if j == 0:
                ax.set_ylabel(f"0MW to {file_values[i]}MW")


plot_variable(files_paths, file_values, variables, axs)
if save_graph:
    plt.savefig(fig_file, dpi=500)
plt.show()
