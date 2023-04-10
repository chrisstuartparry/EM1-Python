from typing import Any, TypeVar
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from EM1PythonClasses import DataProcessor
from EM1PythonDictionaries import (
    parameter_meanings,
    parameter_symbols,
    parameter_units,
    variable_meanings,
    variable_symbols,
    variable_units,
)
import numpy as np


def plot_all(DataProcessor: DataProcessor, variables: list[str]) -> None:
    if not DataProcessor.plot_raw:
        plot_averages  # TODO Finish this function once dependencies are finished


def plot_averages(
    DataProcessor: DataProcessor,
    variables: list[str],
) -> None:
    fig, axs = generate_fig_and_axs(DataProcessor, variables)
    means_stds = get_means_stds(DataProcessor, variables)
    for i, variable in enumerate(variables):
        axs[i].set_title(
            f"{variable_meanings[variable]} vs. {parameter_symbols[DataProcessor.primary_x_parameter]}",
            fontsize=10,
        )
        axs[i].set_xlabel(
            f"{parameter_symbols[DataProcessor.primary_x_parameter]} ({parameter_units[DataProcessor.primary_x_parameter]})"
        )
        axs[i].set_ylabel(f"{variable_symbols[variable]} ({variable_units[variable]})")
        x = means_stds[DataProcessor.primary_x_parameter + "_mean"]
        y = means_stds[variable + "_mean"]
        yerr = means_stds[variable + "_std"]
        axs[i].errorbar(x, y, yerr=yerr, fmt=".", color="black", elinewidth=0.5)
    plt.show()


def generate_fig_and_axs(
    DataProcessor, variables: list[str]
) -> tuple[Figure, list[Axes]]:
    num_variables = len(variables)
    parameter_name = DataProcessor.primary_x_parameter
    ncols: int = 4
    nrows: int = (num_variables + ncols - 1) // ncols

    fig, axs = plt.subplots(
        nrows, ncols, figsize=(15, 5 * nrows), constrained_layout=True
    )
    fig.suptitle(
        f"Averages vs. {parameter_meanings[parameter_name]}",
        fontsize=10,
    )
    axs = axs.flatten()
    return fig, axs


def get_means_stds(
    DataProcessor: DataProcessor, variables: list[str]
) -> dict[Any, Any]:
    means_stds: dict = {}
    for variable in variables:
        variable_means = [
            dataframe[variable].iloc[DataProcessor.start : DataProcessor.end].mean()
            for dataframe in DataProcessor.list_of_dataframes
        ]
        variable_stds = [
            dataframe[variable].iloc[DataProcessor.start : DataProcessor.end].std()
            for dataframe in DataProcessor.list_of_dataframes
        ]
        means_stds[variable + "_mean"] = variable_means
        means_stds[variable + "_std"] = variable_stds
        x_parameter_means = [
            dataframe[DataProcessor.primary_x_parameter]
            .iloc[DataProcessor.start : DataProcessor.end]
            .mean()
            for dataframe in DataProcessor.list_of_dataframes
        ]
        x_parameter_stds = [
            dataframe[DataProcessor.primary_x_parameter]
            .iloc[DataProcessor.start : DataProcessor.end]
            .std()
            for dataframe in DataProcessor.list_of_dataframes
        ]
        means_stds[DataProcessor.primary_x_parameter + "_mean"] = x_parameter_means
        means_stds[DataProcessor.primary_x_parameter + "_std"] = x_parameter_stds
    return means_stds
