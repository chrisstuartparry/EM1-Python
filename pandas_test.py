import scipy.io as sio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter as tk
import tkinter.filedialog as fd
from matplotlib.widgets import Slider
from varname import nameof
from EM1PythonFunctionsNew import generate_fig_and_axs, get_averages_and_stds
from EM1PythonDictionaries import (
    variable_meanings,
    variable_symbols,
    variable_units,
    variable_yticks,
    variables_list,
    parameter_meanings,
    parameter_symbols,
    parameter_units,
    respective_variable_for_dataframe,
)

plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = "\n".join(
    [
        r"\usepackage{siunitx}",
    ]
)


def mat_to_DataFrame(file_path, chosen_structure="post", chosen_substructure="zerod"):
    mat_data = sio.loadmat(file_path)
    structure = mat_data[chosen_structure]
    substructure = structure[chosen_substructure][0, 0]

    # Create a dictionary of the field names and corresponding data, one for arrays and one for scalars

    array_data_dict = {}
    scalar_data_dict = {}
    for field_name in substructure.dtype.names:
        field_data = substructure[field_name][0, 0]
        if field_data.size == 1:
            scalar_data_dict[field_name] = field_data[0]
        else:
            array_data_dict[field_name] = field_data.squeeze()

    # Convert the array dictionary to a pandas DataFrame, and the scalar data to a pandas Series
    df = pd.DataFrame(array_data_dict)
    series = pd.Series(scalar_data_dict)

    return df


def load_data_into_dataframe(file_path):
    default_index_dataframe = mat_to_DataFrame(file_path)
    temps_index_dataframe = default_index_dataframe.set_index("temps")

    for column in temps_index_dataframe.columns:
        if column not in variables_list:
            temps_index_dataframe.drop(column, axis=1, inplace=True)

    temps_index_dataframe["tim"] = (
        temps_index_dataframe["tite"] * temps_index_dataframe["tem"]
    )

    temps_index_dataframe["nTtau"] = (
        temps_index_dataframe["nim"]
        * temps_index_dataframe["tim"]
        * temps_index_dataframe["taue"]
    )

    return temps_index_dataframe


class FilePathListGenerator:
    def __init__(self, base_path, file_name_template, file_values):
        self.base_path = base_path
        self.file_name_template = file_name_template
        self.file_values = file_values

    def generate_file_paths(self):
        return [
            os.path.join(self.base_path, self.file_name_template.format(**value))
            for value in self.file_values
        ]

    def get_file_paths(self, user_decides=False):
        if user_decides:
            root = tk.Tk()
            root.withdraw()
            file_paths = fd.askopenfilenames(parent=root, title="Choose file(s)")
            root.destroy()
        else:
            return self.generate_file_paths()

    def plot_averages(self, x_parameter, dataframes_list, variables, start=50, end=100):
        fig, axs = generate_fig_and_axs(variables, x_parameter)
        averages_and_stds_dict = get_averages_and_stds(dataframes_list, variables)
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
            file_values = self.file_values
            key = list(file_values[0].keys())[0]
            x = [item[key] for item in file_values]
            y = averages_and_stds_dict[variable + "_average"]
            yerr = averages_and_stds_dict[variable + "_std"]
            # print("x:", x, type(x))
            # print("y:", y, type(y))
            # print("yerr:", yerr, type(yerr))
            axs[i].errorbar(x, y, yerr=yerr, fmt=".", color="black", elinewidth=0.5)
        plt.show()


pnbi_file_path_list_generator = FilePathListGenerator(
    base_path="EM1 Data/3rd Run Data (fast mode)",
    file_name_template="2023-01-25 NBI Power {NBI_power}MW.mat",
    file_values=[
        {"NBI_power": value}
        for value in [
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
        ]
        + list(range(2, 41, 2))
    ],
)
pnbi_file_paths = pnbi_file_path_list_generator.get_file_paths(user_decides=False)
pnbi_dataframes = [load_data_into_dataframe(file_path) for file_path in pnbi_file_paths]
# pnbi_dataframes_dictionary = {
#     os.path.basename(file_path): pnbi_dataframe
#     for file_path, pnbi_dataframe in zip(pnbi_file_paths, pnbi_dataframes)
# }

B0_file_path_list_generator = FilePathListGenerator(
    base_path="EM1 Data/4th Run Data (fast mode)",
    file_name_template="2023-01-27 NBI Power 2MW B0 {B0_value}T.mat",
    file_values=[
        {"B0_value": value} for value in (np.array(range(1, 41, 1), dtype=float) / 10)
    ],
)
B0_file_paths = B0_file_path_list_generator.get_file_paths(user_decides=False)
B0_dataframes = [load_data_into_dataframe(file_path) for file_path in B0_file_paths]
# B0_dataframes_dictionary = {
#     os.path.basename(file_path): B0_dataframe
#     for file_path, B0_dataframe in zip(B0_file_paths, B0_dataframes)
# }

Ip_file_path_list_generator = FilePathListGenerator(
    base_path="EM1 Data/5th Run Data (fast mode)/",
    file_name_template="2023-01-31 NBI Power 2MW Ip {Ip_value}MA.mat",
    file_values=[
        {"Ip_value": value} for value in (np.array(range(1, 51, 1), dtype=float) / 10)
    ],
)
Ip_file_paths = Ip_file_path_list_generator.get_file_paths(user_decides=False)
Ip_dataframes = [load_data_into_dataframe(file_path) for file_path in Ip_file_paths]
# Ip_dataframes_dictionary = {
#     os.path.basename(file_path): Ip_dataframe
#     for file_path, Ip_dataframe in zip(Ip_file_paths, Ip_dataframes)
# }

nbar_file_path_list_generator = FilePathListGenerator(
    base_path="EM1 Data/6th Run Data (fast mode)",
    file_name_template="2023-01-31 NBI Power 2MW nbar {nbar_value}.mat",
    file_values=[
        {"nbar_value": value} for value in (np.array(range(1, 41, 1), dtype=float) / 10)
    ],
)
nbar_file_paths = nbar_file_path_list_generator.get_file_paths(user_decides=False)
nbar_dataframes = [load_data_into_dataframe(file_path) for file_path in nbar_file_paths]
# nbar_dataframes_dictionary = {
#     os.path.basename(file_path): nbar_dataframe
#     for file_path, nbar_dataframe in zip(nbar_file_paths, nbar_dataframes)
# }

full_ramp_file_path_list_generator = FilePathListGenerator(
    base_path="EM1 Data/8th Run Data (fast mode)",
    file_name_template=("2023-02-03 NBI Ramping 0 to {last_pnbi_value}MW.mat"),
    file_values=[{"last_pnbi_value": value} for value in np.array(range(2, 11, 2))],
)
full_ramp_file_paths = full_ramp_file_path_list_generator.get_file_paths(
    user_decides=False
)
full_ramp_dataframes = [
    load_data_into_dataframe(file_path) for file_path in full_ramp_file_paths
]
# full_ramp_dataframes_dictionary = {
#     os.path.basename(file_path): full_ramp_dataframe
#     for file_path, full_ramp_dataframe in zip(
#         full_ramp_file_paths, full_ramp_dataframes
#     )
# }

variables = ["nTtau", "ni0", "taue", "tite", "tem"]

pnbi_file_path_list_generator.plot_averages("NBI", pnbi_dataframes, variables)
B0_file_path_list_generator.plot_averages("b0", B0_dataframes, variables)
Ip_file_path_list_generator.plot_averages("Ip", Ip_dataframes, variables)
nbar_file_path_list_generator.plot_averages("Nbar", nbar_dataframes, variables)
