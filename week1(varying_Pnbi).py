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


variables = ["ni0", "tite", "taue", "betap"]
chosen_subsection = "zerod"
start = 50
end = 100
triple_product = True
save_graph = False
if save_graph:
    fig_file = input("Enter the name of the file to save the graph to: ")

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


# for file_path in files_paths:
#     results = get_average(file_path, start, end, variables)
#     for variable, avg, std in results:
#         print(
#             f"Average for variable {variable} in {file_path} is: {avg} +/- {std} (std)"
#         )


# Plot the results


nrows = 1
if triple_product:
    ncols = len(variables) + 1
else:
    ncols = len(variables)
fig, axs = plt.subplots(nrows, ncols, figsize=(15, 5 * nrows), constrained_layout=True)

# fig.suptitle(
#     "Plot of the average of the variables te0, ne0, and taue, recorded on 20/10/22",
#     fontsize=16,
# )


def plot_averages(
    files_paths,
    file_values,
    variables,
    start,
    end,
    axs,
    plot_triple_product,
    x_parameter,
):
    if plot_triple_product:

        axs[0].set_title(
            f"{variable_meanings['nimtimtaue']} vs. {parameter_symbols[x_parameter]}",
            fontsize=10,
        )
        axs[0].set_xlabel(
            f"{parameter_symbols[x_parameter]} ({parameter_units[x_parameter]})"
        )
        axs[0].set_ylabel(
            f'{variable_symbols["nimtimtaue"]} ({variable_units["nimtimtaue"]})'
        )
        for file_path, value in zip(files_paths, file_values):
            results = get_new_triple_product(file_path, start, end)
            triple_product_name, avg, std = results
            axs[0].errorbar(
                value, avg, yerr=std, fmt=".", color="black", elinewidth=0.5
            )
        for i, variable in enumerate(variables):
            axs[i + 1].set_title(
                f"{variable_meanings[variable]} vs. {parameter_symbols[x_parameter]}",
                fontsize=10,
            )
            axs[i + 1].set_xlabel(
                f"{parameter_symbols[x_parameter]} ({parameter_units[x_parameter]})"
            )
            if variable_units[variable] != "":
                axs[i + 1].set_ylabel(
                    f"{variable_symbols[variable]} ({variable_units[variable]})"
                )
            else:
                axs[i + 1].set_ylabel(f"{variable_symbols[variable]}")
            for file_path, value in zip(files_paths, file_values):
                # print(f"Getting data for {variable} at {power} MW")
                results = get_average(file_path, start, end, variables)
                variable, avg, std = results[i]
                # print("Average: ", avg, "Standard Deviation: ", std, "Variable: ", variable)
                # print(f"Plotting {variable} at {power} MW")
                axs[i + 1].errorbar(
                    value, avg, yerr=std, fmt=".", color="black", elinewidth=0.5
                )
    else:
        for i, variable in enumerate(variables):
            axs[i].set_title(
                f"{variable_meanings[variable]} vs. {parameter_symbols[x_parameter]}",
                fontsize=10,
            )
            axs[i].set_xlabel(
                f"{parameter_symbols[x_parameter]} ({parameter_units[x_parameter]})"
            )
            axs[i].set_ylabel(
                f"{variable_symbols[variable]} ({variable_units[variable]})"
            )
            for file_path, value in zip(files_paths, file_values):
                # print(f"Getting data for {variable} at {power} MW")
                results = get_average(file_path, start, end, variables)
                variable, avg, std = results[i]
                # print("Average: ", avg, "Standard Deviation: ", std, "Variable: ", variable)
                # print(f"Plotting {variable} at {power} MW")
                axs[i].errorbar(
                    value, avg, yerr=std, fmt=".", color="black", elinewidth=0.5
                )


plot_averages(
    files_paths,
    file_values,
    variables,
    start,
    end,
    axs,
    plot_triple_product=True,
    x_parameter="NBI",
)

if save_graph:
    plt.savefig(fig_file, dpi=500)
plt.show()
