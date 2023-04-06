import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from pandas import DataFrame
from EM1PythonFunctions import plot_all, load_data_into_dataframe
from EM1PythonClasses import DataProcessor

pnbi_class = DataProcessor(
    base_path="EM1 Data/3rd Run Data (fast mode)",
    file_name_template="NBI Power {}MW.mat",
    primary_x_parameter="pnbi",
)
print(pnbi_class.x_parameter_list)
# print(pnbi_class.list_of_files_via_glob)
