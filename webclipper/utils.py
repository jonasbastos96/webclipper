import os
import re
import shutil


def remove_spaces(text: str):
    text = " ".join(text.split())
    return text


def is_valid_string(text: str):
    result = text and not text.isspace()
    return result


# TODO refactor code
# TODO add exception
def filename_from_url(url: str) -> str:
    filename = re.search("([^/?#]*\.[^/?#]*?$)", url)
    filename = filename.groups()[0]
    return filename


def clear_folder(directory: str):
    files = os.listdir(directory)
    for file in files:
        os.remove(directory + file)


def move_all_folder(origin: str, destiny: str):
    files = os.listdir(origin)
    for file in files:
        past_dir = os.path.join(origin, file)
        new_dir = os.path.join(destiny, file)
        shutil.move(past_dir, new_dir)
