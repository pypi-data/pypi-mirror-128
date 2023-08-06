import os
from .file_io import FileIO
from distutils.dir_util import copy_tree



class Filesystem(FileIO):

    storage_type = os.path.basename(__file__).split('.py')[0]
    
    def __init__(self, storage_type=None):
        super().__init__()

    def upload(self, local_path, remote_path, overwrite=True):
        print("Faking upload because it's running locally.")

    def download(self, remote_path, local_path, overwrite=True):
        copy_tree(remote_path, local_path)
        print("Faking download because it's running locally.")
