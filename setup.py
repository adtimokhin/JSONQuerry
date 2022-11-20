import file_managment as fm
from file_managment import Paths


def default_setup() -> None:
    """
    Creates folders for documents and schemas if they are not present in the data folder

    :return: None
    """
    # By default, we must check whether folders for schemas and documents exist. If they do not, we want to create them
    if not fm.folder_exists(Paths.DOCUMENTS.get_value()):
        fm.create_folder(Paths.DOCUMENTS.get_value())
    if not fm.folder_exists(Paths.SCHEMA.get_value()):
        fm.create_folder(Paths.SCHEMA.get_value())


def clean_start_setup() -> None:
    """
    Removes contents of folders for documents and schemas if they are not present in the data folder.
    Else they will be initialized.

    :return: None
    """
    if fm.folder_exists(Paths.DOCUMENTS.get_value()):
        fm.delete_folder(Paths.DOCUMENTS.get_value())
    fm.create_folder(Paths.DOCUMENTS.get_value())

    if fm.folder_exists(Paths.SCHEMA.get_value()):
        fm.delete_folder(Paths.SCHEMA.get_value())
    fm.create_folder(Paths.SCHEMA.get_value())
