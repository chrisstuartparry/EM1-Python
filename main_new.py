import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import DataFrame
from EM1PythonFunctionsNew import plot_all
from EM1PythonClasses import DataProcessor

# from typing import Iterator

pnbi_class = DataProcessor(
    base_path="EM1 Data/3rd Run Data (fast mode)",
    file_name_template="NBI Power {}MW.mat",
    primary_x_parameter="pnbi",
)
# print(pnbi_class.x_parameter_list)
# print(pnbi_class.list_of_files_via_glob)
# print(len(pnbi_class.list_of_dataframes))

b0_class = DataProcessor(
    base_path="EM1 Data/4th Run Data (fast mode)",
    file_name_template="NBI Power 2MW B0 {}T.mat",
    primary_x_parameter="b0",
)

ip_class = DataProcessor(
    base_path="EM1 Data/5th Run Data (fast mode)/",
    file_name_template="NBI Power 2MW Ip {}MA.mat",
    primary_x_parameter="ip",
)

nbar_class = DataProcessor(
    base_path="EM1 Data/6th Run Data (fast mode)",
    file_name_template="NBI Power 2MW nbar {}.mat",
    primary_x_parameter="nbar",
)

ramping_class = DataProcessor(
    base_path="EM1 Data/8th Run Data (fast mode)",
    file_name_template=("NBI Ramping 0 to {}MW.mat"),
    primary_x_parameter="pnbi",
    subsets=True,
)

DataProcessors = [pnbi_class, b0_class, ip_class, nbar_class, ramping_class]

plot_all(DataProcessors, ["nTtau", "ni0", "taue", "tite", "tem", "pnbi"])
