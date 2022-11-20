import json
import shutil
from enum import Enum
import os.path as op
import os

from typing import List


class Paths(Enum):
    SCHEMA = "schema/",
    DATA_DIRECTORY = './data/',
    DOCUMENTS = "document/",

    def get_value(self):
        return self.value[0]


def file_exists(file_name: str, path: str = "") -> bool:
    """
    Checks whether file with a given name exists in
    a directory that stores all the files.

    :param path: (str) Extra layers of the rooting for a given file. Default=""
    :param file_name: (str) filename without .json
    :return: True is the file exists, else false. (bool)
    """
    try:
        file = open(f"{Paths.DATA_DIRECTORY.get_value()}{path}{file_name}.json", "r")
        file.close()
        return True
    except FileNotFoundError:
        return False


def save_new_file(file_name: str, object_to_save: dict, path: str = "") -> None:
    """
    Saves data passed in new corresponding JSON file.

    :param file_name: (str) filename without .json
    :param object_to_save: (dict) data to save in JSON file
    :param path: (str) Extra layers of the rooting for a given file. Default=""

    :raises FileExistsError if a file with such name already exists
    """
    if file_exists(file_name, path):
        raise FileExistsError

    json_object_to_save = json.dumps(object_to_save, ensure_ascii=False)
    with open(f"{Paths.DATA_DIRECTORY.get_value()}{path}{file_name}.json", "w", encoding="utf8") as f:
        f.write(json_object_to_save)


def rewrite_file(file_name: str, object_to_save: dict, path: str = "") -> None:
    """
    Overwrites data in a JSON file.

    :param file_name: (str) filename without .json
    :param object_to_save: (dict) data to save in JSON file
    :param path: (str) Extra layers of the rooting for a given file. Default=""

    :raises FileNotFoundError if a file with such name does not exist
    """
    if not file_exists(file_name, path):
        raise FileNotFoundError
    json_object_to_save = json.dumps(object_to_save, ensure_ascii=False)
    with open(f"{Paths.DATA_DIRECTORY.get_value()}{path}{file_name}.json", "w", encoding="utf8") as f:
        f.write(json_object_to_save)


def read_file_content(file_name: str, path: str = "") -> dict:
    """
    Returns contents of JSON file as a Python dictionary.

    :param file_name: (str) filename without .json
    :param path: (str) Extra layers of the rooting for a given file. Default=""
    :return: (dict) contents of the JSON file formatted into a dictionary

    :raises FileNotFoundError if a file with such name does not exist
    """
    if not file_exists(file_name, path):
        raise FileNotFoundError

    with open(f"{Paths.DATA_DIRECTORY.get_value()}{path}{file_name}.json", "r") as f:
        data = json.load(f)
    return data


def create_folder(folder_name: str, path: str = "") -> None:
    """
    Creates a new folder inside the DATA_DIRECTORY

    :param folder_name: (str) name of a new folder
    :param path: (str) Extra layers of the rooting for a given file. Default=""

    :raises FileExistsError if a folder with such name already exists
    """
    folder_path = f"{Paths.DATA_DIRECTORY.get_value()}{path}{folder_name}"
    if folder_exists(folder_name, path):
        raise FileExistsError
    os.mkdir(folder_path)


def folder_exists(folder_name: str, path: str = "") -> bool:
    """
    Checks if a folder with by a given path (inside the DATA_DIRECTORY folder) exists.

    :param folder_name: (str) name of a new folder
    :param path: (str) Extra layers of the rooting for a given file. Default=""

    :return: (bool) True if the folder exists, False if does not.
    """
    folder_path = f"{Paths.DATA_DIRECTORY.get_value()}{path}{folder_name}"
    return op.isdir(folder_path)


def get_all_file_names(folder_name: str) -> List[str]:
    """
    Returns a list containing all files in a given folder. Filenames will contains their filetype.

    :param folder_name: (str) name of a new folder. Must contain directions
                       starting, but not including, the DATA_DIRECTORY folder

    :return: List[str] a list of the filenames
    """
    folder_path = f"{Paths.DATA_DIRECTORY.get_value()}{folder_name}"
    return os.listdir(folder_path)


def delete_file(file_name: str, path: str = "") -> None:
    """
    Deletes a given file by its unique filename. File of extension .json will be deleted.

    :param file_name: (str) filename without .json
    :param path: (str) Extra layers of the rooting for a given file. Default=""

    :raises FileNotFoundError if the does not exist in a specified location.
    """
    if not file_exists(file_name, path):
        raise FileNotFoundError
    file_path = f"{Paths.DATA_DIRECTORY.get_value()}{path}{file_name}.json"
    os.remove(file_path)


def delete_folder(folder_name: str, path: str = "") -> None:
    """
    Deletes a folder with all of its contents, using the path specified.
    If there is an exception thrown, an appropriate message will be displayed in console.

    :param folder_name:  (str) name of a new folder. Must contain directions
                       starting, but not including, the DATA_DIRECTORY folder
    :param path: (str) Extra layers of the rooting for a given file. Default=""
    """
    folder_path = f"{Paths.DATA_DIRECTORY.get_value()}{path}{folder_name}"
    try:
        shutil.rmtree(folder_path)
    except Exception as e:
        print('Failed to delete files in %s. Reason: %s' % (folder_path, e))
