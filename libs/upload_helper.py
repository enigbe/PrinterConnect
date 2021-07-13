import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

# Basic neutral CAD files
CAD_MODELS = tuple('stp step stl igs iges x_t x_b vrml x3d dae dxf ipt'.split())
IMAGE_SET = UploadSet('images', IMAGES)
CAD_MODEL_SET = UploadSet('models', CAD_MODELS)


def save_upload(uploaded_set: UploadSet, file: FileStorage, folder: str = None, name: str = None) -> str:
    """Takes an uploaded set, a FileStorage object and saves it to a folder"""
    return uploaded_set.save(file, folder, name)


def get_path(uploaded_set: UploadSet, filename: str, folder: str) -> str:
    """Takes an uploaded set, file name and folder. Returns the full path"""
    return uploaded_set.path(filename, folder)


def find_upload_any_format(uploaded_set: UploadSet, filename: str, folder: str) -> Union[str, None]:
    """Takes a filename and folder, and returns an image in any of the accepted formats"""

    def __uploaded_file_extension(extension_tuple):
        for _format in extension_tuple:
            file_name = f"{filename}.{_format}"
            file_path = IMAGE_SET.path(filename=file_name, folder=folder)
            if os.path.isfile(file_path):
                return file_path
        return None

    if uploaded_set == IMAGE_SET:
        return __uploaded_file_extension(IMAGES)

    if uploaded_set == CAD_MODEL_SET:
        return __uploaded_file_extension(CAD_MODELS)


def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """Take a FileStorage and return the filename"""
    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    """Check our regex and return whether the string matches or not"""
    filename = _retrieve_filename(file)

    allowed_format = '|'.join(IMAGES)  # png|svg|jpg...
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def get_basename(file: Union[str, FileStorage]) -> str:
    """Return full name of image in the path"""
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file: Union[str, FileStorage]) -> str:
    """Return file extension"""
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
