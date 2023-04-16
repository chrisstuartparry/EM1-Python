from typing import Any
import matplotlib.pyplot as plt
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

plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = "\n".join(
    [
        r"\usepackage{siunitx}",
    ]
)


def plot_averages(
    DataProcessor: DataProcessor,
    variables: list[str],
) -> None:
    fig, axs = generate_fig_and_axs(DataProcessor, variables)
    means_stds = get_means_stds(DataProcessor, variables)

    index = 0
    nrows, ncols = axs.shape

    loop_flag = True
    for row in range(nrows):
        for col in range(ncols):
            if index >= len(variables):
                loop_flag = False
                for i in range(col, ncols):
                    axs[row, i].axis("off")
                break
            variable = variables[index]
            axs[row, col].set_title(
                f"{variable_meanings[variable]} vs. {parameter_symbols[DataProcessor.primary_x_parameter]}",
                fontsize=10,
            )
            axs[row, col].set_xlabel(
                f"{parameter_symbols[DataProcessor.primary_x_parameter]} ({parameter_units[DataProcessor.primary_x_parameter]})"
            )
            axs[row, col].set_ylabel(
                f"{variable_symbols[variable]} ({variable_units[variable]})"
            )
            x = means_stds[DataProcessor.primary_x_parameter + "_mean"]
            y = means_stds[variable + "_mean"]
            yerr = means_stds[variable + "_std"]
            axs[row, col].errorbar(
                x, y, yerr=yerr, fmt=".", color="black", elinewidth=0.5
            )
            index += 1
        if not loop_flag:
            break
    # for i, variable in enumerate(variables):
    #     axs[i].set_title(
    #         f"{variable_meanings[variable]} vs. {parameter_symbols[DataProcessor.primary_x_parameter]}",
    #         fontsize=10,
    #     )
    # axs[i].set_xlabel(
    #     f"{parameter_symbols[DataProcessor.primary_x_parameter]} ({parameter_units[DataProcessor.primary_x_parameter]})"
    # )
    #     axs[i].set_ylabel(f"{variable_symbols[variable]} ({variable_units[variable]})")
    #     x = means_stds[DataProcessor.primary_x_parameter + "_mean"]
    #     y = means_stds[variable + "_mean"]
    #     yerr = means_stds[variable + "_std"]
    #     axs[i].errorbar(x, y, yerr=yerr, fmt=".", color="black", elinewidth=0.5)
    plt.plot()


def generate_fig_and_axs(DataProcessor, variables: list[str]) -> tuple[Figure, Any]:
    num_variables = len(variables)
    parameter_name = DataProcessor.primary_x_parameter
    ncols: int = 4
    nrows: int = (num_variables + ncols - 1) // ncols
    fig: Figure
    axs: Any
    fig, axs = plt.subplots(
        nrows, ncols, figsize=(15, 5 * nrows), constrained_layout=True, squeeze=False
    )
    fig.suptitle(
        f"Averages vs. {parameter_meanings[parameter_name]}",
        fontsize=10,
    )
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


def generate_fig_and_axes_subsets(DataProcessor: DataProcessor, variables: list[str]):
    nrows: int = len(DataProcessor.list_of_dataframes)
    ncols: int = len(variables)
    fig, axs = plt.subplots(
        nrows, ncols, figsize=(15, 5 * nrows), constrained_layout=True
    )
    return fig, axs


def draw_subsets_all_subsets(
    DataProcessor: DataProcessor, variables: list[str], axs, temps=False
):
    if not temps:
        x_parameter = DataProcessor.primary_x_parameter
    else:
        x_parameter = "temps"
    for i, dataframe in enumerate(DataProcessor.list_of_dataframes):
        for j, variable in enumerate(variables):
            ax = axs[i, j]
            if variable_units[variable] != "":
                if i == 0:
                    ax.set_title(
                        f"{variable_meanings[variable]} against {variable_meanings[x_parameter]}"
                    )
                ax.set_xlabel(
                    f"{variable_symbols[x_parameter]} ({variable_units[x_parameter]})"
                )
                ax.set_ylabel(
                    f"{variable_symbols[variable]} ({variable_units[variable]})"
                )
            else:
                if i == 0:
                    ax.set_title(
                        f"{variable_meanings[variable]} against {variable_meanings[x_parameter]}"
                    )
                ax.set_xlabel(
                    f"{variable_symbols[x_parameter]} ({variable_units[x_parameter]})"
                )
                ax.set_ylabel(f"{variable_symbols[variable]}")
            x = dataframe[x_parameter]
            y = dataframe[variable].tolist()
            ax.plot(x, y, ".", color="black")
    plt.plot()


def plot_ramping_all_subsets(
    DataProcessor: DataProcessor, variables: list[str], temps=False
):
    fig, axs = generate_fig_and_axes_subsets(DataProcessor, variables)
    if temps:
        draw_subsets_all_subsets(DataProcessor, variables, axs, temps=True)
    else:
        draw_subsets_all_subsets(DataProcessor, variables, axs, temps=False)


def plot_all(DataProcessorList: list[DataProcessor], variables: list[str]):
    for DataProcessor in DataProcessorList:
        if DataProcessor.subsets:
            plot_ramping_all_subsets(DataProcessor, variables, temps=False)
            plot_ramping_all_subsets(DataProcessor, variables, temps=True)
        else:
            plot_averages(DataProcessor, variables)
    plt.show()
