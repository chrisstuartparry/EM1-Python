import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import os
from EM1PythonFunctions import get_average, get_triple_product, get_variable

plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = "\n".join(
    [
        r"\usepackage{siunitx}",
    ]
)

chosen_subsection = "zerod"
variables = ["taue", "betan", "modeh", "qeff"]
# variables = ["taue", "q0", "q95", "qeff"]
variable_symbols = {
    "taue": r"$\tau_E$",
    "betan": r"$\beta_{\mathrm{normalised}}$",
    "modeh": r"H-Mode",
    "qeff": r"$q_{\mathrm{effective}}$",
    "q0": r"$q_0$",
    "q95": r"$q_{95}$",
    "temps": r"$t$",
    "pnbi": r"$PNBI_{\mathrm{input}}$",
    "frnbi": r"$PNBI_{\mathrm{frac absorbed in plasma}}$",
    "ip:": r"$I_{\mathrm{plasma}}$",
    "betap": r"$\beta_{\mathrm{poloidal}}$",
    "nbar": r"$\bar{n}$",
    "ne0": r"$n_{e(0)}$",
    "ni0": r"$n_{i(0)}$",
    "pfus": r"$P_{\mathrm{fusion}}$",
    "sext": r"$S_{\mathrm{external}}$",
    "vp": r"$V_{\mathrm{plasma}}$",
    "W": r"$E_{\mathrm{total in plasma}}$",
}

variable_units = {
    "taue": r"\unit{\second}",
    "betan": "",
    "modeh": "",
    "qeff": "",
    "q0": "",
    "q95": "",
    "temps": r"\unit{\second}",
    "pnbi": r"\unit{\watt}",
    "frnbi": "",
    "ip:": r"$\unit{ampere}$",
    "betap": "",
    "nbar": "",
    "ne0": "",
    "ni0": "",
    "pfus": r"\unit{\watt}",
    "sext": r"\unit{\metre\squared}",
    "vp": r"\unit{\metre\cubed}",
    "W": r"\unit{\joule}",
}

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
                    ax.set_title(
                        f'{variable_symbols[variable]} ({variable_units[variable]}) against Time ({variable_units["temps"]})'
                    )
            else:
                if i == 0:
                    ax.set_title(
                        f'{variable_symbols[variable]} against Time ({variable_units["temps"]})'
                    )
            time_results = get_variable(file_path, ["temps"])
            times = time_results[0][1]
            results = get_variable(file_path, variables)
            variable, ydata = results[j]
            ax.plot(times, ydata, ".", color="black")
            if i == nrows - 1:
                ax.set_xlabel("Time (s)")
            if j == 0:
                ax.set_ylabel(f"{first_file_values[i]}MW to {last_file_values[i]}MW")


plot_variable(files_paths, first_file_values, last_file_values, variables, axs)
if save_graph:
    plt.savefig(fig_file, dpi=500)
plt.show()
