import os

__package_dir = os.path.abspath(os.path.dirname(__file__))
__parent_dir = os.path.abspath(os.path.dirname(__package_dir))
__root_dir = os.path.abspath(os.path.dirname(__parent_dir))

database = os.path.join(__parent_dir, 'databases\\database.db')
temp_folder = os.path.join(__parent_dir, 'temp\\')
