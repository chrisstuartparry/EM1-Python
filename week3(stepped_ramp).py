import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import os
from EM1PythonFunctions import get_average, get_triple_product, get_variable
from EM1PythonDictionaries import variable_symbols, variable_units, variable_meanings

plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = "\n".join(
    [
        r"\usepackage{siunitx}",
    ]
)

chosen_subsection = "zerod"
# variables = ["taue", "betan", "modeh", "qeff"]
variables = ["taue", "q0", "q95", "qeff"]


start = 50
end = 100
save_graph = False
if save_graph:
    fig_file = input("Enter the name of the file to save the graph to: ")

base_path = "EM1 Data/7th Run Data (fast mode)"
file_name_template = (
    "2023-02-03 NBI Ramping {first_pnbi_value} to {last_pnbi_value}MW.mat"
)
first_file_values = np.array(range(0, 9, 2))
last_file_values = np.array(range(2, 11, 2))

files_paths = [
    os.path.join(
        base_path,
        file_name_template.format(
            first_pnbi_value=first_value, last_pnbi_value=last_value
        ),
    )
    for first_value, last_value in zip(first_file_values, last_file_values)
]


nrows = len(files_paths)
ncols = len(variables)
fig, axs = plt.subplots(nrows, ncols, figsize=(15, 5 * nrows), constrained_layout=True)
# plt.rcParams["figure.dpi"] = 150  # Sets the resolution of the figure (dots per inch)
fig.suptitle(
    "Plots of the chosen variables against Time (s)",
    fontsize=16,
)


def plot_variable(files_paths, first_file_values, last_file_values, variables, axs):
    for i, file_path in enumerate(files_paths):
        for j, variable in enumerate(variables):
            ax = axs[i, j]
            if variable_units[variable] != "":
                if i == 0:
                    ax.set_title(f"{variable_meanings[variable]} against Time")

                ax.set_ylabel(
                    f"{variable_symbols[variable]} ({variable_units[variable]})"
                )
            else:
                if i == 0:
                    ax.set_title(f"{variable_meanings[variable]} against Time")
                ax.set_ylabel(f"{variable_symbols[variable]}")
            time_results = get_variable(file_path, ["temps"])
            times = time_results[0][1]
            results = get_variable(file_path, variables)
            variable, ydata = results[j]
            ax.plot(times, ydata, ".", color="black")
            if i == nrows - 1:
                ax.set_xlabel(f'{variable_symbols["temps"]} {variable_units["temps"]}')


plot_variable(files_paths, first_file_values, last_file_values, variables, axs)
if save_graph:
    plt.savefig(fig_file, dpi=500)
plt.show()
