import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import os
from EM1PythonDictionaries import (
    variable_meanings,
    variable_symbols,
    variable_units,
    parameter_meanings,
    parameter_symbols,
    parameter_units,
)


def get_variable(file_path, variables, chosen_subsection="zerod"):
    full_dataset = scipy.io.loadmat(file_path)
    results = []
    for variable in variables:
        a = full_dataset["post"][chosen_subsection][0][0][variable][0][0]
        a = [float(x[0]) for x in a]
        results.append([variable, a])
    return results


def get_average(file_path, start, end, variables, chosen_subsection="zerod"):
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


def get_new_triple_product(file_path, start, end):
    full_dataset = scipy.io.loadmat(file_path)
    progenitor_variables = ["tite", "tem"]
    # multiply ti/te by te to get ti:
    progenitor_results_raw = get_variable(file_path, progenitor_variables)
    ti = np.array(progenitor_results_raw[0][1]) * np.array(progenitor_results_raw[1][1])
    progenitor_results_name = ["ti"]
    progenitor_results_mean = np.mean(ti[start:end])
    progenitor_results_std = np.std(ti[start:end])
    progenitor_results_total = [
        progenitor_results_name,
        progenitor_results_mean,
        progenitor_results_std,
    ]
    remaining_triple_product_variables = ["ni0", "taue"]
    results = []
    for variable in remaining_triple_product_variables:
        a = full_dataset["post"]["zerod"][0][0][variable][0][0]
        a = [float(x[0]) for x in a]
        avg = np.mean(a[start:end])
        std = np.std(a[start:end])
        results.append([variable, avg, std])
    triple_product_avg = progenitor_results_total[1] * results[0][1] * results[1][1]
    triple_product_std = triple_product_avg * np.sqrt(
        (progenitor_results_total[2] / progenitor_results_total[1]) ** 2
        + (results[0][2] / results[0][1]) ** 2
        + (results[1][2] / results[1][1]) ** 2
    )
    return ["triple_product", triple_product_avg, triple_product_std]


def plot_variable(
    files_paths,
    first_file_values,
    last_file_values,
    variables,
    axs,
    row_header_yesno=True,
):
    row_headers = []
    for i, file_path in enumerate(files_paths):
        for j, variable in enumerate(variables):
            ax = axs[i, j]
            if variable_units[variable] != "":
                if i == 0:
                    ax.set_title(
                        f"{variable_meanings[variable]} against {variable_meanings['temps']}"
                    )

                ax.set_ylabel(
                    f"{variable_symbols[variable]} ({variable_units[variable]})"
                )
            else:
                if i == 0:
                    ax.set_title(
                        f"{variable_meanings[variable]} against {variable_meanings['temps']}"
                    )
                ax.set_ylabel(f"{variable_symbols[variable]}")
            time_results = get_variable(file_path, ["temps"])
            times = time_results[0][1]
            results = get_variable(file_path, variables)
            variable, ydata = results[j]
            ax.plot(times, ydata, ".", color="black")
            ax.set_xlabel(f'{variable_symbols["temps"]} ({variable_units["temps"]})')
        if row_header_yesno:
            row_headers.append(f"{first_file_values[i]}MW to {last_file_values[i]}MW")
    return row_headers


def add_headers(
    fig,
    *,
    row_headers=None,
    col_headers=None,
    row_pad=1,
    col_pad=5,
    rotate_row_headers=True,
    **text_kwargs,
):
    """
    Function to add row and column headers to a matplotlib figure.

    Based on https://stackoverflow.com/a/25814386

    Args:
        fig (_type_): The figure which contains the axes to work on
        row_headers (_type_, optional):  A sequence of strings to be row headers. Defaults to None.
        col_headers (_type_, optional): A sequence of strings to be column headers. Defaults to None.
        row_pad (int, optional): Value to adjust padding. Defaults to 1.
        col_pad (int, optional): Value to adjust padding. Defaults to 5.
        rotate_row_headers (bool, optional): Whether to rotate by 90° the row headers. Defaults to True.
        **text_kwargs: Forwarded to ax.annotate(...)
    """

    axes = fig.get_axes()

    for ax in axes:
        sbs = ax.get_subplotspec()

        # Putting headers on cols
        if (col_headers is not None) and sbs.is_first_row():
            ax.annotate(
                col_headers[sbs.colspan.start],
                xy=(0.5, 1),
                xytext=(0, col_pad),
                xycoords="axes fraction",
                textcoords="offset points",
                ha="center",
                va="baseline",
                **text_kwargs,
            )

        # Putting headers on rows
        if (row_headers is not None) and sbs.is_first_col():
            ax.annotate(
                row_headers[sbs.rowspan.start],
                xy=(0, 0.5),
                xytext=(-ax.yaxis.labelpad - row_pad, 0),
                xycoords=ax.yaxis.label,
                textcoords="offset points",
                ha="right",
                va="center",
                rotation=rotate_row_headers * 90,
                **text_kwargs,
            )


def plot_averages(
    files_paths,
    file_values,
    variables,
    start,
    end,
    axs,
    plot_triple_product,
    x_parameter,
):
    if plot_triple_product:
        axs[0].set_title(
            f"{variable_meanings['nimtimtaue']} vs. {parameter_symbols[x_parameter]}",
            fontsize=10,
        )
        axs[0].set_xlabel(
            f"{parameter_symbols[x_parameter]} ({parameter_units[x_parameter]})"
        )
        axs[0].set_ylabel(
            f'{variable_symbols["nimtimtaue"]} ({variable_units["nimtimtaue"]})'
        )
        for file_path, value in zip(files_paths, file_values):
            results = get_new_triple_product(file_path, start, end)
            triple_product_name, avg, std = results
            axs[0].errorbar(
                value, avg, yerr=std, fmt=".", color="black", elinewidth=0.5
            )
        for i, variable in enumerate(variables):
            axs[i + 1].set_title(
                f"{variable_meanings[variable]} vs. {parameter_symbols[x_parameter]}",
                fontsize=10,
            )
            axs[i + 1].set_xlabel(
                f"{parameter_symbols[x_parameter]} ({parameter_units[x_parameter]})"
            )
            if variable_units[variable] != "":
                axs[i + 1].set_ylabel(
                    f"{variable_symbols[variable]} ({variable_units[variable]})"
                )
            else:
                axs[i + 1].set_ylabel(f"{variable_symbols[variable]}")
            for file_path, value in zip(files_paths, file_values):
                # print(f"Getting data for {variable} at {power} MW")
                results = get_average(file_path, start, end, variables)
                variable, avg, std = results[i]
                # print("Average: ", avg, "Standard Deviation: ", std, "Variable: ", variable)
                # print(f"Plotting {variable} at {power} MW")
                axs[i + 1].errorbar(
                    value, avg, yerr=std, fmt=".", color="black", elinewidth=0.5
                )
    else:
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
            for file_path, value in zip(files_paths, file_values):
                results = get_average(file_path, start, end, variables)
                variable, avg, std = results[i]
                axs[i].errorbar(
                    value, avg, yerr=std, fmt=".", color="black", elinewidth=0.5
                )
