import os

from webclipper import utils

__package_dir = os.path.abspath(os.path.dirname(__file__))
__parent_dir = os.path.abspath(os.path.dirname(__package_dir))

# Root folder of application
root_dir = os.path.abspath(os.path.dirname(__parent_dir))
# Database
database = os.path.join(__parent_dir, 'databases\\database.db')

# Temporary Folder
temp_folder = os.path.join(__parent_dir, 'temp\\')

# Check if folder exists
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)
else:
    utils.clear_folder(temp_folder)
