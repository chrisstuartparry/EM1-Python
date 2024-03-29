from EM1PythonClasses import DataProcessor
from EM1PythonFunctions import plot_all

# Define the DataProcessors below

pnbi_class_default = DataProcessor(
    base_path="EM1 Data/3rd Run Data (fast mode)",
    file_name_template="NBI Power {}MW.mat",
    primary_x_parameter="pnbi",
)

b0_class_2MW = DataProcessor(
    base_path="EM1 Data/4th Run Data (fast mode)",
    file_name_template="NBI Power 2MW B0 {}T.mat",
    primary_x_parameter="b0",
)

ip_class_2MW = DataProcessor(
    base_path="EM1 Data/5th Run Data (fast mode)/",
    file_name_template="NBI Power 2MW Ip {}MA.mat",
    primary_x_parameter="ip",
)

nbar_class_2MW = DataProcessor(
    base_path="EM1 Data/6th Run Data (fast mode)",
    file_name_template="NBI Power 2MW nbar {}.mat",
    primary_x_parameter="nbar",
)

maximising_pnbi_class = DataProcessor(
    base_path="EM1 Data/9th Run Data (fast mode)",
    file_name_template="NBI Power 2MW Max {}.mat",
    primary_x_parameter="temps",
    subsets=True,
)

ramping_class_default = DataProcessor(
    base_path="EM1 Data/8th Run Data (fast mode)",
    file_name_template=("NBI Ramping 0 to {}MW.mat"),
    primary_x_parameter="pnbi",
    subsets=True,
)

# Define the list of DataProcessors to be plotted
DataProcessors = [
    pnbi_class_default,
    b0_class_2MW,
    ip_class_2MW,
    nbar_class_2MW,
    ramping_class_default,
    maximising_pnbi_class,
]

# variables = [
#     "nTtau",
#     "ni0",
#     "taue",
#     "nbar",
#     "ni0",
#     "nim",
#     "ne0",
#     "te0",
#     "tem",
#     "tite",
#     "tim",
#     "modeh",
# ]
# variables = ["nbar", "ni0", "nim", "ne0"]
# variables = [
#     "te0",
#     "tem",
#     "tite",
#     "tim",
# ]
# variables = ["ne0", "te0", "taue", "ne0te0taue", "nim", "tim", "taue", "nimtimtaue"]
# variables = ["ne0", "te0", "taue", "ne0te0taue"]
# variables = ["ne0"]
# variables = ["taue"]
variables = ["ne0te0taue"]

#  Plot the data
plot_all(DataProcessors, variables)
