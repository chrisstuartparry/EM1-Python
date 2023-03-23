import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from EM1PythonFunctions import (
    get_average,
    get_triple_product,
    get_new_triple_product,
    get_variable,
    plot_variable,
    add_headers,
)
from EM1PythonDictionaries import variable_symbols, variable_units, variable_meanings

Tk().withdraw()
plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = "\n".join(
    [
        r"\usepackage{siunitx}",
    ]
)

chosen_subsection = "zerod"
variables = ["taue", "betan", "modeh", "qeff"]
start = 50
end = 100

# select a file to import
files_paths = [askopenfilename()]
file_value = 2
nrows = len(files_paths)
ncols = len(variables)
fig, axs = plt.subplots(nrows, ncols, figsize=(15, 5 * nrows), constrained_layout=True)
print(axs)

triple_product_value = get_new_triple_product(files_paths[0], start, end)

print(f"Triple Product:{triple_product_value}")


def plot_variable_singluar(files_paths, file_value, variables, axs):
    for i, file_path in enumerate(files_paths):
        for j, variable in enumerate(variables):
            ax = axs[j]
            if variable_units[variable] != "":
                if i == 0:
                    ax.set_title(
                        f"{variable_meanings[variable]} against {variable_meanings['temps']}"
                    )

                ax.set_ylabel(
                    f"{variable_symbols[variable]} ({variable_units[variable]})"
                )
            else:
                if i == 0:
                    ax.set_title(
                        f"{variable_meanings[variable]} against {variable_meanings['temps']}"
                    )
                ax.set_ylabel(f"{variable_symbols[variable]}")
            time_results = get_variable(file_path, ["temps"])
            times = time_results[0][1]
            results = get_variable(file_path, variables)
            variable, ydata = results[j]
            ax.plot(times, ydata, ".", color="black")
            ax.set_xlabel(f'{variable_symbols["temps"]} ({variable_units["temps"]})')


plot_variable_singluar(files_paths, file_value, variables, axs)
plt.show()
