import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import DataFrame
from EM1PythonFunctionsNew import plot_averages
from EM1PythonClasses import DataProcessor

pnbi_class = DataProcessor(
    base_path="EM1 Data/3rd Run Data (fast mode)",
    file_name_template="NBI Power {}MW.mat",
    primary_x_parameter="pnbi",
)
print(pnbi_class.x_parameter_list)
print(pnbi_class.list_of_files_via_glob)
print(len(pnbi_class.list_of_dataframes))

plot_averages(pnbi_class, ["nTtau", "ni0", "taue", "tite", "tem"])
