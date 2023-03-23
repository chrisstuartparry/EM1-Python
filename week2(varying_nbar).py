import scipy.io
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

variables = ["taue", "betan", "modeh", "qeff"]
# variables = ["taue", "q0", "q95", "qeff"]
chosen_subsection = "zerod"
triple_product = True
start = 50
end = 100


base_path = "EM1 Data/6th Run Data (fast mode)"
file_name_template = "2023-01-31 NBI Power 2MW nbar {nbar_value}.mat"
file_values = np.array(range(1, 41, 1), dtype=float) / 10

files_paths = [
    os.path.join(base_path, file_name_template.format(nbar_value=value))
    for value in file_values
]

nrows = 1
if triple_product:
    ncols = len(variables) + 1
else:
    ncols = len(variables)
fig, axs = plt.subplots(nrows, ncols, figsize=(15, 5 * nrows), constrained_layout=True)

plot_averages(
    files_paths,
    file_values,
    variables,
    start,
    end,
    axs,
    plot_triple_product=True,
    x_parameter="Nbar",
)


plt.show()
