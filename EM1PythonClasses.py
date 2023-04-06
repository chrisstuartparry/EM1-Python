import os
import tkinter as tk
import tkinter.filedialog as fd
import glob
import re


class FilePathListGenerator:
    def __init__(
        self,
        base_path: str,
        file_name_template: str,
        file_values: list[dict[str, float]],
        ramping=False,
    ):
        self.base_path: str = base_path
        self.file_name_template: str = file_name_template
        self.file_values: list[dict[str, float]] = file_values
        self.ramping: bool = ramping

    def generate_file_paths(self) -> list[str]:
        return [
            os.path.join(self.base_path, self.file_name_template.format(**value))
            for value in self.file_values
        ]

    def get_file_paths(self, user_decides=False) -> list[str]:
        # if user_decides:
        #     root = tk.Tk()
        #     root.withdraw()
        #     file_paths: tuple[str, ...] | Literal[''] = fd.askopenfilenames(parent=root, title="Choose file(s)")
        #     root.destroy()
        #     return file_paths
        # else:
        return self.generate_file_paths()


class DataProcessor:
    def __init__(
        self, base_path: str, file_name_template: str, primary_x_parameter: str
    ) -> None:
        self.base_path = base_path
        self.file_name_template = file_name_template
        self.glob_file_name_template = file_name_template.format("*")
        self.primary_x_parameter = primary_x_parameter
        self.x_parameter_list: list[dict[str, float]] = self.generate_x_parameter_list()
        self.list_of_files_via_glob: list[str] = self.get_files_list()

    def get_files_list(self) -> list[str]:
        glob_file_path = os.path.join(self.base_path, self.glob_file_name_template)
        list_of_files_via_glob = sorted(glob.glob(glob_file_path))
        return list_of_files_via_glob

    def generate_x_parameter_list(self) -> list[dict[str, float]]:
        files_list: list[str] = self.get_files_list()
        regex_pattern = self.file_name_template.format(r"(\d+(\.\d+)?)")

        x_parameter_list = [
            {f"{self.primary_x_parameter}": float(match.group(1))}
            for file in files_list
            if (match := re.search(regex_pattern, file))
        ]
        return x_parameter_list
