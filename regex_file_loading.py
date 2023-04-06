# import glob
# import re
# import os
# from typing import LiteralString

# # pnbi example
# base_path: str = "EM1 Data/3rd Run Data (fast mode)"
# file_name_template = "NBI Power {pnbi}MW.mat"
# # glob_file_name_template = "NBI Power *MW.mat"
# glob_file_name_template = file_name_template.format("*")
# glob_file_path = os.path.join(base_path, glob_file_name_template)
# list_of_files_via_glob: list[str] = glob.glob(glob_file_path)

# pnbi_list: list[dict[str, float]] = [
#     {"pnbi": float(match.group(1))}
#     for file in list_of_files_via_glob
#     if (match := re.search(r"NBI Power (\d+)MW.mat", file))
# ]
# print(pnbi_list)


import glob
import re
import os
from typing import LiteralString

base_path: str = "EM1 Data/3rd Run Data (fast mode)"
file_name_template = "NBI Power {}MW.mat"
glob_file_name_template = file_name_template.format("*")
glob_file_path = os.path.join(base_path, glob_file_name_template)
list_of_files_via_glob: list[str] = glob.glob(glob_file_path)
list_of_files_via_glob = sorted(list_of_files_via_glob)
print(list_of_files_via_glob)
print(len(list_of_files_via_glob))
primary_x_parameter: str = "pnbi"
pnbi_list: list[dict[str, float]] = [
    {f"{primary_x_parameter}": float(match.group(1))}
    for file in list_of_files_via_glob
    if (match := re.search(r"NBI Power (\d+(\.\d+)?)MW.mat", file))
]
print(pnbi_list)
print(len(pnbi_list))
# r"(\d+(\.\d+)?)"
