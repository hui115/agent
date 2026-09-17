
import os

def get_project_root()->str:
    current_file=os.path.abspath(__file__)
    current_dir=os.path.dirname(current_file)
    current_project=os.path.dirname(current_dir)
    return current_project


def get_abs_path(relative_path:str)->str:
    current_project=get_project_root()
    return os.path.join(current_project,relative_path)



