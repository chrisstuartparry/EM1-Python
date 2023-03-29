import os
import tkinter as tk
import tkinter.filedialog as fd
from varname import nameof


class FilePathListGenerator:
    def __init__(self, base_path, file_name_template, file_values, ramping=False):
        self.base_path = base_path
        self.file_name_template = file_name_template
        self.file_values = file_values
        self.ramping = ramping

    def generate_file_paths(self):
        return [
            os.path.join(self.base_path, self.file_name_template.format(**value))
            for value in self.file_values
        ]

    def get_file_paths(self, user_decides=False):
        if user_decides:
            root = tk.Tk()
            root.withdraw()
            file_paths = fd.askopenfilenames(parent=root, title="Choose file(s)")
            root.destroy()
            return file_paths
        else:
            return self.generate_file_paths()
