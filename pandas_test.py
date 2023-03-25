import scipy.io as sio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from EM1PythonDictionaries import (
    variable_meanings,
    variable_symbols,
    variable_units,
    variable_yticks,
    variables_list,
    parameter_meanings,
    parameter_symbols,
    parameter_units,
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


def load_data(file_path):
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


file_path = "EM1 Data/4th Run Data (fast mode)/2023-01-27 NBI Power 2MW B0 0.1T.mat"
dataframe = load_data(file_path)
print(dataframe)
