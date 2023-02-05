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


fig, axs = plt.subplots(
    len(files_paths), len(variables), figsize=(15, 5 * len(files_paths))
)
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


def plot_variable(files_paths, variables, axs):
    for j, file_path in enumerate(files_paths):
        for i, variable in enumerate(variables):
            ax = axs[j, i]
            ax.set_title(f"{variable}")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel(variable)

            time_results = get_variable(file_path, ["temps"])
            times = time_results[0][1]
            results = get_variable(file_path, variables)
            variable, ydata = results[i]
            # print(
            #     f"times: {times}, times type: {type(times)} \n ydata: {ydata}, ydata type: {type(ydata)}, \n variable: {variable}, variable type: {type(variable)}"
            # )
            ax.plot(times, ydata, ".", color="black")


plot_variable(files_paths, variables, axs)
if save_graph:
    plt.savefig(fig_file, dpi=500)
plt.show()
