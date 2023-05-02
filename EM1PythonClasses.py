import os
import glob
import re
import scipy.io as sio
import pandas as pd
from pandas import DataFrame
from EM1PythonDictionaries import variables_list


class DataProcessor:
    start = 50
    end = 100

    def __init__(
        self,
        base_path: str,
        file_name_template: str,
        primary_x_parameter: str,
        plot_raw: bool = False,
        subsets: bool = False,
    ) -> None:
        self.base_path = base_path
        self.file_name_template = file_name_template
        self.glob_file_name_template = file_name_template.format("*")
        self.primary_x_parameter = primary_x_parameter
        self.x_parameter_list: list[dict[str, float]] = self.generate_x_parameter_list()
        self.list_of_files_via_glob: list[str] = self.get_files_list()
        self.list_of_dataframes: list[DataFrame] = self.generate_dataframes_list()
        self.plot_raw = plot_raw
        self.subsets = subsets

    def get_files_list(self) -> list[str]:
        glob_file_path = os.path.join(self.base_path, self.glob_file_name_template)
        list_of_files_via_glob = glob.glob(glob_file_path)
        regex_pattern = self.file_name_template.format(r"(\d+(\.\d+)?)")
        list_of_files_via_glob.sort(
            key=lambda file: float(match.group(1))
            if (match := re.search(regex_pattern, file))
            else 0
        )
        return list_of_files_via_glob

    def get_matched_elements(self) -> tuple[list[float], list[int]]:
        regex_pattern = self.file_name_template.format(r"(\d+(\.\d+)?)")
        matched_elements = [
            float(match[1])
            for file in self.list_of_files_via_glob
            if (match := re.search(regex_pattern, file))
        ]
        matched_elements_int = [int(element) for element in matched_elements]
        return matched_elements, matched_elements_int

    def generate_x_parameter_list(self) -> list[dict[str, float]]:
        # sourcery skip: inline-immediately-returned-variable, use-getitem-for-re-match-groups  # noqa: E501
        files_list: list[str] = self.get_files_list()
        regex_pattern = self.file_name_template.format(r"(\d+(\.\d+)?)")

        x_parameter_list = [
            {f"{self.primary_x_parameter}": float(match.group(1))}
            for file in files_list
            if (match := re.search(regex_pattern, file))
        ]
        return x_parameter_list

    def mat_to_DataFrame(
        self,
        file_path,
        chosen_structure="post",
        chosen_substructure="zerod",
        chosen_subsubstructure=None,
    ) -> DataFrame:
        array_data_dict = {}
        scalar_data_dict = {}
        if chosen_subsubstructure is not None:
            substructure = self.get_substructure(
                file_path, chosen_structure, chosen_substructure
            )
            subsubstructure = substructure[chosen_subsubstructure][0, 0]
            for field_name in subsubstructure.dtype.names:
                field_data = subsubstructure[field_name][0, 0]
                if field_data.size == 1:
                    scalar_data_dict[field_name] = field_data[0]
                else:
                    array_data_dict[field_name] = field_data.squeeze()
        else:
            substructure = self.get_substructure(
                file_path, chosen_structure, chosen_substructure
            )
            for field_name in substructure.dtype.names:
                field_data = substructure[field_name][0, 0]
                if field_data.size == 1:
                    scalar_data_dict[field_name] = field_data[0]
                else:
                    array_data_dict[field_name] = field_data.squeeze()

        return pd.DataFrame(array_data_dict)

    def get_substructure(self, file_path, chosen_structure, chosen_substructure):
        mat_data = sio.loadmat(file_path)
        structure = mat_data[chosen_structure]
        return structure[chosen_substructure][0, 0]

    def load_data_into_dataframe(self, file_path) -> DataFrame:
        file_dataframe: DataFrame = self.mat_to_DataFrame(file_path)
        file_dataframe = file_dataframe.filter(items=variables_list)
        file_dataframe["tim"] = file_dataframe["tite"] * file_dataframe["tem"]
        file_dataframe["nimtimtaue"] = (
            file_dataframe["nim"] * file_dataframe["tim"] * file_dataframe["taue"]
        )
        file_dataframe["ne0te0taue"] = (
            file_dataframe["ne0"] * file_dataframe["te0"] * file_dataframe["taue"]
        )
        file_dataframe["nTtau"] = file_dataframe["ne0te0taue"]
        dataframe_for_b0: DataFrame = self.mat_to_DataFrame(
            file_path,
            chosen_structure="post",
            chosen_substructure="z0dinput",
            chosen_subsubstructure="geo",
        )
        dataframe_for_b0 = dataframe_for_b0.filter(items=["b0"])
        file_dataframe["b0"] = dataframe_for_b0["b0"]
        return file_dataframe

    def generate_dataframes_list(self) -> list[DataFrame]:
        return [
            self.load_data_into_dataframe(file_path)
            for file_path in self.list_of_files_via_glob
        ]
