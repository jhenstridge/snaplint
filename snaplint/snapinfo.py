
import functools
import os

import yaml

__all__ = ['SnapInfo']

class SnapInfo:

    def __init__(self, path):
        # Make sure path ends in a separator to make things easier
        self.path = os.path.join(path, '')

    @functools.lru_cache()
    def snap_yaml():
        """Return the decoded meta/snap.yaml"""
        with open(os.path.join(self.path, "meta", "snap.yaml"), 'rb') as fp:
            return yaml.safe_load(fp)

    def get_file_list(self):
        '''Return a list of files in the snap'''
        file_list = []
        for root, dirs, files in os.walk(self.path):
            for f in files:
                file_list.append(os.path.relpath(os.path.join(root, f),
                                                 self.path))

        return file_list

    def get_dir_list(self):
        '''Return a list of directories in the snap'''
        dir_list = []
        for root, dirs, files in os.walk(self.path):
            for d in dirs:
                dir_list.append(os.path.relpath(os.path.join(root, d),
                                                self.path))
        return dir_list
