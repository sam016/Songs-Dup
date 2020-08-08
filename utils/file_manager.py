"""
Contains FS related function
"""

import os
import re


def get_files(directory, extensions=None):
    """Gets the list of files in a directory and sub-directory

    Args:
        directory (str): path of directory
        extensions (List[str]): list of extensions to search
    """

    match_ext = "^.+(" + '|'.join(extensions) + ")$" if extensions else None
    count_dirs = 0
    count_files = 0
    count_match_files = 0
    files = []

    for root, _, files in os.walk(directory):
        count_dirs += 1
        for file in files:
            count_files += 1
            if match_ext is not None or re.match(match_ext, file):
                count_match_files += 1
                files.append((root, file, os.path.join(root, file)))

    return (files, count_dirs, count_files, count_match_files)
