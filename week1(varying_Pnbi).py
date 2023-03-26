import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import os
from EM1PythonFunctions import show_plot_averages
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


show_plot_averages(files_paths, file_values, variables, "NBI")
