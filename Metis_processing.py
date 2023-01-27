import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import os

# from matplotlib.widgets import CheckButtons

chosen_subsection = "zerod"
triple_product = True
save_graph = False
if save_graph:
    fig_file = input("Enter the name of the file to save the graph to: ")

# load the data


base_path = "EM1 Data/Third Run Data (fast mode)"
file_name_template = "2023-01-25 NBI Power {NBI_power}MW.mat"
NBI_powers = [0, 0.25, 0.5, 0.75, 1]+list(
    range(2, 41, 2)
)  # generates a list of NBI powers from 2 to 41 in steps of 2

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


def get_triple_product(file_path, start, end):
    full_dataset = scipy.io.loadmat(file_path)
    ne0 = full_dataset["post"][chosen_subsection][0][0]["ne0"][0][0]
    ne0 = [float(x[0]) for x in ne0]
    te0 = full_dataset["post"][chosen_subsection][0][0]["te0"][0][0]
    te0 = [float(x[0]) for x in te0]
    taue = full_dataset["post"][chosen_subsection][0][0]["taue"][0][0]
    taue = [float(x[0]) for x in taue]
    ne0_avg = np.mean(ne0[start:end])
    te0_avg = np.mean(te0[start:end])
    taue_avg = np.mean(taue[start:end])
    ne0_std = np.std(ne0[start:end])
    te0_std = np.std(te0[start:end])
    taue_std = np.std(taue[start:end])
    triple_product_avg = ne0_avg * te0_avg * taue_avg
    triple_product_std = triple_product_avg * np.sqrt(
        (ne0_std / ne0_avg) ** 2 + (te0_std / te0_avg) ** 2 + (taue_std / taue_avg) ** 2
    )
    return ["triple_product", triple_product_avg, triple_product_std]


variables = ["ne0", "te0", "taue", "betap"]
start = 50
end = 100

# for file_path in files_paths:
#     results = get_average(file_path, start, end, variables)
#     for variable, avg, std in results:
#         print(
#             f"Average for variable {variable} in {file_path} is: {avg} +/- {std} (std)"
#         )


# Plot the results
if triple_product:
    fig, axs = plt.subplots(1, len(variables) + 1, figsize=(18, 6))
else:
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

if triple_product:
    # Add a new subplot for the triple product
    axs[0].set_title("Triple Product")
    axs[0].set_xlabel("Power (MW)")
    axs[0].set_ylabel("nTtaue")
    for file_path, power in zip(files_paths, NBI_powers):
        results = get_triple_product(file_path, start, end)
        triple_product, avg, std = results
        axs[0].errorbar(power, avg, yerr=std, fmt="o", color="black")
    for i, variable in enumerate(variables):
        # axs[i].set_title(variable)
        axs[i+1].set_xlabel("Power (MW)")
        axs[i+1].set_ylabel(variable)
        for file_path, power in zip(files_paths, NBI_powers):
            # print(f"Getting data for {variable} at {power} MW")
            results = get_average(file_path, start, end, variables)
            variable, avg, std = results[i]
            # print("Average: ", avg, "Standard Deviation: ", std, "Variable: ", variable)
            # print(f"Plotting {variable} at {power} MW")
            axs[i+1].errorbar(power, avg, yerr=std, fmt="o", color="black")
else:
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
fig.tight_layout()
if save_graph:
    plt.savefig(fig_file, dpi=500)

plt.show()
