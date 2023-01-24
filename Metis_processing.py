import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.widgets import CheckButtons

chosen_subsection = "zerod"
save_graph = False
if save_graph:
    fig_file = input("Enter the name of the file to save the graph to: ")

# load the data


base_path = "EM1 Data/Second Run Data (standard mode)/"
file_name_template = "2023-01-20 NBI Power {NBI_power}MW.mat"
NBI_powers = list(
    range(2, 41, 2)
)  # generates a list of powers from 2 to 40 in steps of 2

files_paths = [
    os.path.join(base_path, file_name_template.format(NBI_power=power))
    for power in NBI_powers
]



def get_average(file_path, start, end, variables):
    full_dataset = scipy.io.loadmat(file_path)
    results = []
    for variable in variables:
        a = full_dataset["post"][chosen_subsection][0][0][variable][0][0]
        a = [float(x[0]) for x in a]
        avg = np.mean(a[start:end])
        std = np.std(a[start:end])
        results.append([variable, avg, std])
    return results


variables = ["te0", "ne0", "taue"]
start = 50
end = 100

# for file_path in files_paths:
#     results = get_average(file_path, start, end, variables)
#     for variable, avg, std in results:
#         print(
#             f"Average for variable {variable} in {file_path} is: {avg} +/- {std} (std)"
#         )


# Plot the results
fig, axs = plt.subplots(1, len(variables), figsize=(18, 6))
plt.rcParams["figure.dpi"] = 150  # Sets the resolution of the figure (dots per inch)
plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = "\n".join(
    [
        r"\usepackage{siunitx}",
    ]
)
# fig.suptitle(
#     "Plot of the average of the variables te0, ne0, and taue, recorded on 20/10/22",
#     fontsize=16,
# )
for i, variable in enumerate(variables):
    # axs[i].set_title(variable)
    axs[i].set_xlabel("Power (MW)")
    axs[i].set_ylabel(variable)
    for file_path, power in zip(files_paths, NBI_powers):
        # print(f"Getting data for {variable} at {power} MW")
        results = get_average(file_path, start, end, variables)
        variable, avg, std = results[i]
        # print("Average: ", avg, "Standard Deviation: ", std, "Variable: ", variable)
        # print(f"Plotting {variable} at {power} MW")
        axs[i].errorbar(power, avg, yerr=std, fmt="o", color="black") 

if save_graph:
    plt.savefig(fig_file, dpi=500)

plt.show()
