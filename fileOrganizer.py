import os
from pathlib import Path
import shutil

base_dir = r"D:\edu\University\Term2\AP\myDir"

ext = {
    "png": "Images",
    "jpeg": "Images",
    "jpg": "Images",
    "jfif": "Images",
    "gif": "Images",
    "mp4": "Videos",
    "pdf": "PDFFiles",
    "py": "PythonFiles",
}


def makeDirs(dir_name):
    os.mkdir(Path(base_dir) / dir_name)


for name in ["Images", "Videos", "PDFFiles", "PythonFiles"]:
    makeDirs(name)

files = os.listdir(Path(base_dir))

for file in files:
    try:
        file_ext = file[file.index(".") + 1 :]
        target_dir = Path(base_dir) / ext[file_ext]
        shutil.copy(Path(base_dir) / file, target_dir)
        os.remove(Path(base_dir) / file)
    except:
        pass
