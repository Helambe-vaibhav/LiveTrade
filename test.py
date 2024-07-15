import os
import pathlib

path = 'D:\PROJECTS\ResumeProjects\LiveTrade\L_Trade'

# get me file structure in tree format
def get_file_structure(path):
    path = pathlib.Path(path)
    for item in path.iterdir():
        if item.is_file():
            print(item.name)
        else:
            print(f"{item.name}/")
            get_file_structure(item)

get_file_structure(path)

