import scipy.io as sio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from varname import nameof
from matplotlib.widgets import RadioButtons
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


def plot_interactive(file_path_list_generators, dataframes_lists, variables):
    def update_plot(label):
        for file_path_list_generator, dataframes_list, axs_group in zip(
            file_path_list_generators, dataframes_lists, axs_groups
        ):
            visible = file_path_list_generator.base_path == label
            for axs in axs_group:
                for ax in axs:
                    ax.set_visible(visible)
        plt.draw()

    # Create the figures and axes
    axs_groups = [
        generate_fig_and_axs(variables, nameof(file_path_list_generator.file_values[0]))
        for file_path_list_generator in file_path_list_generators
    ]
    # Plot the data
    for file_path_list_generator, dataframes_list, axs_group in zip(
        file_path_list_generators, dataframes_lists, axs_groups
    ):
        x_parameter = nameof(file_path_list_generator.file_values[0])
        averages_and_stds_dict = get_averages_and_stds(dataframes_list, variables)
        for i, variable in enumerate(variables):
            axs = axs_group[1][i]
            axs.set_title(
                f"{variable_meanings[variable]} vs. {parameter_symbols[x_parameter]}",
                fontsize=10,
            )
            axs.set_xlabel(
                f"{parameter_symbols[x_parameter]} ({parameter_units[x_parameter]})"
            )
            axs.set_ylabel(f"{variable_symbols[variable]} ({variable_units[variable]})")
            file_values = file_path_list_generator.file_values
            key = list(file_values[0].keys())[0]
            x = [item[key] for item in file_values]
            y = averages_and_stds_dict[variable + "_average"]
            yerr = averages_and_stds_dict[variable + "_std"]
            axs.errorbar(x, y, yerr=yerr, fmt=".", color="black", elinewidth=0.5)
            axs.set_visible(False)

    # Set the first set of axes as visible
    for ax in axs_groups[0][1]:
        ax.set_visible(True)

    # Create the radio button widget
    ax_radio = plt.axes([0.05, 0.4, 0.1, 0.15])
    radio = RadioButtons(
        ax_radio,
        [
            nameof(file_path_list_generator.file_values[0])
            for file_path_list_generator in file_path_list_generators
        ],
    )

    # Connect the radio buttons to the update_plot function
    radio.on_clicked(update_plot)

    # Display the plot with the interactive widget
    plt.show()
