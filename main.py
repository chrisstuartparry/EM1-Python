import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from pandas import DataFrame
from EM1PythonFunctionsNew import plot_all, load_data_into_dataframe
from EM1PythonClasses import FilePathListGenerator

start_time = datetime.now()

plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = "\n".join(
    [
        r"\usepackage{siunitx}",
    ]
)


pnbi_file_path_list_generator = FilePathListGenerator(
    base_path="EM1 Data/3rd Run Data (fast mode)",
    file_name_template="NBI Power {pnbi}MW.mat",
    file_values=[
        {"pnbi": value}
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
pnbi_file_paths: list[str] = pnbi_file_path_list_generator.get_file_paths(
    user_decides=False
)
pnbi_dataframes: list[DataFrame] = [
    load_data_into_dataframe(file_path) for file_path in pnbi_file_paths
]
# pnbi_dataframes_dictionary = {
#     os.path.basename(file_path): pnbi_dataframe
#     for file_path, pnbi_dataframe in zip(pnbi_file_paths, pnbi_dataframes)
# }

B0_file_path_list_generator = FilePathListGenerator(
    base_path="EM1 Data/4th Run Data (fast mode)",
    file_name_template="NBI Power 2MW B0 {b0}T.mat",
    file_values=[
        {"b0": value} for value in (np.array(range(1, 41, 1), dtype=float) / 10)
    ],
)
B0_file_paths: list[str] = B0_file_path_list_generator.get_file_paths(
    user_decides=False
)
B0_dataframes: list[DataFrame] = [
    load_data_into_dataframe(file_path) for file_path in B0_file_paths
]
# B0_dataframes_dictionary = {
#     os.path.basename(file_path): B0_dataframe
#     for file_path, B0_dataframe in zip(B0_file_paths, B0_dataframes)
# }

Ip_file_path_list_generator = FilePathListGenerator(
    base_path="EM1 Data/5th Run Data (fast mode)/",
    file_name_template="NBI Power 2MW Ip {ip}MA.mat",
    file_values=[
        {"ip": value} for value in (np.array(range(1, 51, 1), dtype=float) / 10)
    ],
)
Ip_file_paths: list[str] = Ip_file_path_list_generator.get_file_paths(
    user_decides=False
)
Ip_dataframes: list[DataFrame] = [
    load_data_into_dataframe(file_path) for file_path in Ip_file_paths
]
# Ip_dataframes_dictionary = {
#     os.path.basename(file_path): Ip_dataframe
#     for file_path, Ip_dataframe in zip(Ip_file_paths, Ip_dataframes)
# }

nbar_file_path_list_generator = FilePathListGenerator(
    base_path="EM1 Data/6th Run Data (fast mode)",
    file_name_template="NBI Power 2MW nbar {nim}.mat",
    file_values=[
        {"nim": value} for value in (np.array(range(1, 41, 1), dtype=float) / 10)
    ],
)
nbar_file_paths: list[str] = nbar_file_path_list_generator.get_file_paths(
    user_decides=False
)
nbar_dataframes: list[DataFrame] = [
    load_data_into_dataframe(file_path) for file_path in nbar_file_paths
]
# nbar_dataframes_dictionary = {
#     os.path.basename(file_path): nbar_dataframe
#     for file_path, nbar_dataframe in zip(nbar_file_paths, nbar_dataframes)
# }

full_ramp_file_path_list_generator = FilePathListGenerator(
    base_path="EM1 Data/8th Run Data (fast mode)",
    file_name_template=("NBI Ramping 0 to {pnbi}MW.mat"),
    file_values=[{"pnbi": value} for value in np.array(range(2, 11, 2))],
    ramping=True,
)
full_ramp_file_paths: list[str] = full_ramp_file_path_list_generator.get_file_paths(
    user_decides=False
)
full_ramp_dataframes: list[DataFrame] = [
    load_data_into_dataframe(file_path) for file_path in full_ramp_file_paths
]
# full_ramp_dataframes_dictionary = {
#     os.path.basename(file_path): full_ramp_dataframe
#     for file_path, full_ramp_dataframe in zip(
#         full_ramp_file_paths, full_ramp_dataframes
#     )
# }

variables: list[str] = ["nTtau", "ni0", "taue", "tite", "tem"]

file_path_list_generators_to_plot: list[FilePathListGenerator] = [
    pnbi_file_path_list_generator,
    B0_file_path_list_generator,
    Ip_file_path_list_generator,
    nbar_file_path_list_generator,
    full_ramp_file_path_list_generator,
]

dataframes_lists_to_plot: list[list[DataFrame]] = [
    pnbi_dataframes,
    B0_dataframes,
    Ip_dataframes,
    nbar_dataframes,
    full_ramp_dataframes,
]

plot_all(file_path_list_generators_to_plot, dataframes_lists_to_plot, variables)
print(f"Done in {datetime.now() - start_time}")

# TODO Add code to analyse whichever files are in a certain folder. Hints to do this are in recent ChatGPT chat "Configuring file selection with JSON.". Don't use JSON, though.
