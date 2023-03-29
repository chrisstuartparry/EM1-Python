import scipy.io as sio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from varname import nameof
from EM1PythonDictionaries import (
    variable_meanings,
    variable_symbols,
    variable_units,
    variables_list,
    parameter_meanings,
    parameter_symbols,
    parameter_units,
)


def generate_fig_and_axs(variables, parameter_name):
    nrows = 1
    ncols = len(variables)
    fig, axs = plt.subplots(
        nrows, ncols, figsize=(15, 5 * nrows), constrained_layout=True
    )
    fig.suptitle(
        f"Averages vs. {parameter_meanings[parameter_name]}",
        fontsize=10,
    )
    return fig, axs


def get_averages_and_stds(dataframes_list, variables, start=50, end=100):

    averages_and_stds = {}
    for variable in variables:
        variable_averages = [
            dataframe[variable].iloc[start:end].mean() for dataframe in dataframes_list
        ]
        variable_stds = [
            dataframe[variable].iloc[start:end].std() for dataframe in dataframes_list
        ]
        averages_and_stds[variable + "_average"] = variable_averages
        averages_and_stds[variable + "_std"] = variable_stds
    return averages_and_stds


def plot_averages(
    file_path_list_generator, x_parameter, dataframes_list, variables, start=50, end=100
):
    fig, axs = generate_fig_and_axs(variables, x_parameter)
    averages_and_stds_dict = get_averages_and_stds(
        dataframes_list, variables, start, end
    )
    for i, variable in enumerate(variables):
        axs[i].set_title(
            f"{variable_meanings[variable]} vs. {parameter_symbols[x_parameter]}",
            fontsize=10,
        )
        axs[i].set_xlabel(
            f"{parameter_symbols[x_parameter]} ({parameter_units[x_parameter]})"
        )
        axs[i].set_ylabel(f"{variable_symbols[variable]} ({variable_units[variable]})")
        file_values = file_path_list_generator.file_values
        key = list(file_values[0].keys())[0]
        x = [item[key] for item in file_values]
        y = averages_and_stds_dict[variable + "_average"]
        yerr = averages_and_stds_dict[variable + "_std"]
        axs[i].errorbar(x, y, yerr=yerr, fmt=".", color="black", elinewidth=0.5)
    plt.plot()


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


def plot_all4(file_path_list_generators, dataframes_lists, variables):
    for file_path_list_generator, dataframes_list in zip(
        file_path_list_generators, dataframes_lists
    ):
        x_parameter = list(file_path_list_generator.file_values[0].keys())[0]
        print("x_parameter: ", x_parameter)
        plot_averages(file_path_list_generator, x_parameter, dataframes_list, variables)
    plt.show()
