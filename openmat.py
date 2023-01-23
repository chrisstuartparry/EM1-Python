import scipy.io


mat = scipy.io.loadmat(
    "EM1 Data/Second Run Data (standard mode)/2023-01-20 NBI Power 2MW.mat",
    variable_names=["post"],
)

variable_name = input("Enter the name of the variable to display: ")
if variable_name in mat:
    print(mat[variable_name])
else:
    print("Variable not found in file.")


import scipy.io

filename = input("Enter the name of the .mat file: ")
mat = scipy.io.loadmat(filename)

variable_path = input(
    "Enter the path of the variable to display (e.g. 'subsection1/subsection2/variable_name'): "
)

# Split the input string on the '/' character to get the list of keys
keys = variable_path.split("/")

# Use a for loop to navigate the nested dictionaries and get the value of the specified variable
value = mat
for key in keys:
    if key in value:
        value = value[key]
    else:
        print("Variable not found in file.")
        exit()

print(value)
