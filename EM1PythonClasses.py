import os
import tkinter as tk
import tkinter.filedialog as fd
from typing import Literal


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
