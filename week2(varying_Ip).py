import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import os

chosen_subsection = "zerod"
variables = ["taue", "betan", "modeh", "qeff"]
start = 50
end = 100
save_graph = False
if save_graph:
    fig_file = input("Enter the name of the file to save the graph to: ")

base_path = "EM1 Data/th Run Data (fast mode)"
file_name_template = " NBI Power 2MW Ip {Ip}.mat"
Ip_values = np.array(range(1,51,1), dtype=float)/10

files_paths = [
    os.path.join(base_path, file_name_template.format(Ip=value))
    for value in Ip_values
]



def get_triple_product(file_path, start, end):
    full_dataset = scipy.io.loadmat(file_path)
    triple_product_variables = ["ni0", "tite", "taue"]
    results = []
    for variable in triple_product_variables:
        a = full_dataset["post"]["zerod"][0][0][variable][0][0]
        a = [float(x[0]) for x in a]
        avg = np.mean(a[start:end])
        std = np.std(a[start:end])
        results.append([variable, avg, std])
    triple_product_avg = results[0][1] * results[1][1] * results[2][1]
    triple_product_std = triple_product_avg * np.sqrt(
        (results[0][2] / results[0][1]) ** 2
        + (results[1][2] / results[1][1]) ** 2
        + (results[2][2] / results[2][1]) ** 2
    )
    return ["triple_product", triple_product_avg, triple_product_std]

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

fig, axs = plt.subplots(1, len(variables) + 1, figsize=(15, 5))
plt.rcParams["figure.dpi"] = 150  # Sets the resolution of the figure (dots per inch)
plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = "\n".join(
    [
        r"\usepackage{siunitx}",
    ]
)
fig.suptitle(
    "Plots of the average values of the chosen variables against Ip at an NBI power of 2 MW",
    fontsize=16,
)
axs[0].set_title("Triple Product")
axs[0].set_xlabel("Ip ()")
axs[0].set_ylabel("nTtaue")
for file_path, power in zip(files_paths, Ip_values):
    results = get_triple_product(file_path, start, end)
    triple_product, avg, std = results
    axs[0].errorbar(power, avg, yerr=std, fmt=".", color="black", elinewidth=0.5)
for i, variable in enumerate(variables):
    axs[i+1].set_title(f"{variable}")
    axs[i+1].set_xlabel("Power (MW)")
    axs[i+1].set_ylabel(variable)
    for file_path, power in zip(files_paths, Ip_values):
        # print(f"Getting data for {variable} at {power} MW")
        results = get_average(file_path, start, end, variables)
        variable, avg, std = results[i]
        # print("Average: ", avg, "Standard Deviation: ", std, "Variable: ", variable)
        # print(f"Plotting {variable} at {power} MW")
        axs[i+1].errorbar(power, avg, yerr=std, fmt=".", color="black", elinewidth=0.5)
fig.tight_layout()
if save_graph:
    plt.savefig(fig_file, dpi=500)
plt.show()