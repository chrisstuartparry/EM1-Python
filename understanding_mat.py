import scipy.io as sio
import cProfile, pstats
from datetime import datetime
import numpy.lib.recfunctions as rfn

start_time = datetime.now()
file_path = "EM1 Data/8th Run Data (fast mode)/2023-02-03 NBI Ramping 0 to 10MW.mat"


def mat_to_DataFrame(file_path, chosen_structure="post", chosen_substructure="zerod"):
    mat_data = sio.loadmat(file_path, squeeze_me=False)
    structure = mat_data[chosen_structure]
    print("Datatype of structure array:", structure.dtype)
    print("Shape of structure array:", structure.shape)

    substructure = structure[chosen_substructure][0, 0]
    print("Datatype of substructure array:", substructure.dtype)
    print("Shape of substructure array:", substructure.shape)
    print("Substructure datatype names: ", substructure.dtype.names)


# cProfile.run("mat_to_DataFrame(file_path)")

# pstats.Stats(
#     cProfile.Profile().run("mat_to_DataFrame(file_path)")
# ).strip_dirs().sort_stats(pstats.SortKey.CUMULATIVE).print_stats(20)

mat_to_DataFrame(file_path)

print(f"Done in {datetime.now() - start_time}")
