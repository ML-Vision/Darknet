import os
from pathlib import Path as mypath

def model_json_path():
    return mypath.joinpath(model_root(),"models.json")

def model_root():
    return mypath.joinpath(mypath.cwd(),"models")

def model_names():
    result = os.listdir(model_root())
    if 'models.json' in result:
        result.remove("models.json")
    return result

def inner_file_path(one,two,three):
    return mypath.joinpath(mypath.joinpath(one,two),three)

def join_path(one,two):
    return mypath.joinpath(one,two)

def cur_path():
    return mypath.cwd()

def test_image_path():
    return join_path(mypath.cwd(),"test_image")

def str_to_path(s):
    return mypath(s)

def Image_Train_folders():
    return os.listdir(join_path(mypath.cwd(),"Image_to_Train"))