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
    parameter_meanings,
    parameter_symbols,
    parameter_units,
)
from EM1PythonClasses import FilePathListGenerator


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
