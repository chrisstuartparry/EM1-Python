import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import os
from EM1PythonFunctions import (
    get_average,
    get_triple_product,
    get_variable,
    plot_variable,
    add_headers,
    get_new_triple_product,
    plot_averages,
)
from EM1PythonDictionaries import (
    variable_meanings,
    variable_symbols,
    variable_units,
    parameter_meanings,
    parameter_symbols,
    parameter_units,
)

plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = "\n".join(
    [
        r"\usepackage{siunitx}",
    ]
)


# variables = ["ni0", "taue", "betan", "modeh", "qeff"]
variables = ["ni0", "taue", "tite", "tem"]
chosen_subsection = "zerod"
triple_product = True


# load the data


base_path = "EM1 Data/3rd Run Data (fast mode)"
file_name_template = "2023-01-25 NBI Power {NBI_power}MW.mat"
file_values = [
    0,
    0.25,
    0.5,
    0.75,
    1,
    1.1,
    1.2,
    1.3,
    1.4,
    1.5,
    1.6,
    1.7,
    1.8,
    1.9,
] + list(
    range(2, 41, 2)
)  # generates a list of NBI powers from 2 to 41 in steps of 2

files_paths = [
    os.path.join(base_path, file_name_template.format(NBI_power=power))
    for power in file_values
]


nrows = 1
if triple_product:
    ncols = len(variables) + 1
else:
    ncols = len(variables)
fig, axs = plt.subplots(nrows, ncols, figsize=(15, 5 * nrows), constrained_layout=True)

fig.suptitle(
    f"Averages vs. {parameter_meanings['NBI']}",
    fontsize=10,
)


plot_averages(
    files_paths,
    file_values,
    variables,
    axs,
    plot_triple_product=True,
    x_parameter="NBI",
)


plt.show()
