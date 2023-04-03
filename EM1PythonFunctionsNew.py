import scipy.io as sio
import pandas as pd
import matplotlib.pyplot as plt
from EM1PythonDictionaries import (
    variable_meanings,
    variable_symbols,
    variable_units,
    variables_list,
    parameter_meanings,
    parameter_symbols,
    parameter_units,
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

    # Create a dictionary of the field names & data, one for arrays and one for scalars

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
    # series = pd.Series(scalar_data_dict)

    return df


def load_data_into_dataframe(file_path):
    file_dataframe = mat_to_DataFrame(file_path)
    file_dataframe = file_dataframe.filter(items=variables_list)

    file_dataframe["tim"] = file_dataframe["tite"] * file_dataframe["tem"]

    file_dataframe["nTtau"] = (
        file_dataframe["nim"] * file_dataframe["tim"] * file_dataframe["taue"]
    )

    return file_dataframe


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


def get_averages_and_stds(dataframes_list, x_parameter, variables, start=50, end=100):
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
    if x_parameter != "b0":
        x_parameter_average = [
            dataframe[x_parameter].iloc[start:end].mean()
            for dataframe in dataframes_list
        ]
        x_parameter_std = [
            dataframe[x_parameter].iloc[start:end].std()
            for dataframe in dataframes_list
        ]
        averages_and_stds[x_parameter + "_average"] = x_parameter_average
        averages_and_stds[x_parameter + "_std"] = x_parameter_std
    return averages_and_stds


def plot_averages(
    file_path_list_generator, x_parameter, dataframes_list, variables, start=50, end=100
):
    fig, axs = generate_fig_and_axs(variables, x_parameter)
    averages_and_stds_dict = get_averages_and_stds(
        dataframes_list, x_parameter, variables, start, end
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
        # file_values = file_path_list_generator.file_values
        # key = list(file_values[0].keys())[0]
        # x = [item[key] for item in file_values]
        if x_parameter == "b0":
            file_values = file_path_list_generator.file_values
            key = list(file_values[0].keys())[0]
            x = [item[key] for item in file_values]
        else:
            x = averages_and_stds_dict[x_parameter + "_average"]
        y = averages_and_stds_dict[variable + "_average"]
        yerr = averages_and_stds_dict[variable + "_std"]
        axs[i].errorbar(x, y, yerr=yerr, fmt=".", color="black", elinewidth=0.5)
    plt.plot()


def generate_fig_and_axes_ramping(dataframes_list, variables, parameter_name):
    nrows = len(dataframes_list)
    ncols = len(variables)
    fig, axs = plt.subplots(
        nrows, ncols, figsize=(15, 5 * nrows), constrained_layout=True
    )
    # fig.suptitle(f"Ramping Plots", fontsize=10)
    return fig, axs


def plot_ramping(file_path_list_generator, x_parameter, dataframes_list, variables):
    fig, axs = generate_fig_and_axes_ramping(dataframes_list, variables, x_parameter)
    row_headers = []
    x_parameter = list(file_path_list_generator.file_values[0].keys())[0]
    for i, dataframe in enumerate(dataframes_list):
        for j, variable in enumerate(variables):
            ax = axs[i, j]
            if variable_units[variable] != "":
                if i == 0:
                    ax.set_title(
                        f"{variable_meanings[variable]} against\
                            {variable_meanings[x_parameter]}"
                    )

                ax.set_ylabel(
                    f"{variable_symbols[variable]} ({variable_units[variable]})"
                )
            else:
                if i == 0:
                    ax.set_title(
                        f"{variable_meanings[variable]} against\
                        {variable_meanings[x_parameter]}"
                    )
                ax.set_ylabel(f"{variable_symbols[variable]}")
            x = dataframe[x_parameter]
            y = dataframe[variable].tolist()
            ax.plot(x, y, ".", color="black")
        row_headers.append(
            f"0MW to {list(file_path_list_generator.file_values[i].values())[0]}MW"
        )
    add_headers(fig, row_headers=row_headers)
    plt.plot()


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
        row_headers (_type_, optional):  A sequence of strings to be row headers.
            Defaults to None.
        col_headers (_type_, optional): A sequence of strings to be column headers.
            Defaults to None.
        row_pad (int, optional): Value to adjust padding. Defaults to 1.
        col_pad (int, optional): Value to adjust padding. Defaults to 5.
        rotate_row_headers (bool, optional): Whether to rotate by 90° the row headers.
            Defaults to True.
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


def plot_all(file_path_list_generators, dataframes_lists, variables):
    for file_path_list_generator, dataframes_list in zip(
        file_path_list_generators, dataframes_lists
    ):
        x_parameter = list(file_path_list_generator.file_values[0].keys())[0]
        # print("x_parameter: ", x_parameter)
        # print("file_path_list_generator.ramping: ", file_path_list_generator.ramping)
        if not file_path_list_generator.ramping:
            plot_averages(
                file_path_list_generator, x_parameter, dataframes_list, variables
            )
        elif file_path_list_generator.ramping:
            plot_ramping(
                file_path_list_generator, x_parameter, dataframes_list, variables
            )
        elif file_path_list_generator.ramping is None:
            raise AttributeError(
                "file_path_list_generator ramping attribute must exist (and be True or False)"
            )
        else:
            raise ValueError(
                "file_path_list_generator ramping attribute must be True or False"
            )
    plt.show(block=False)
    # plt.show()
