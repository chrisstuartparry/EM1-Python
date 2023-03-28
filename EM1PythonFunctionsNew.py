import scipy.io as sio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from varname import nameof
from matplotlib.widgets import Slider
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


# def get_averages_and_stds(dataframes_list, variables, start=50, end=100):

#     averages_and_stds = {}
#     for variable in variables:
#         variable_averages = [
#             dataframe[variable].iloc[start:end].mean() for dataframe in dataframes_list
#         ]
#         variable_stds = [
#             dataframe[variable].iloc[start:end].std() for dataframe in dataframes_list
#         ]
#         averages_and_stds[variable + "_average"] = variable_averages
#         averages_and_stds[variable + "_std"] = variable_stds
#     return averages_and_stds


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
