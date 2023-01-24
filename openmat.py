import scipy.io

filename = "EM1 Data/Second Run Data (standard mode)/2023-01-20 NBI Power 2MW.mat" 
mat = scipy.io.loadmat(filename)

variable_path = "post/zerod/te0"

# Split the input string on the '/' character to get the list of keys
keys = variable_path.split('/')

# Use a for loop to navigate the nested dictionaries and get the value of the specified variable
value = mat
for key in keys:
    if key in value:
        value = value[key]
    else:
        print("Variable not found in file.")
        exit()

print(value)
