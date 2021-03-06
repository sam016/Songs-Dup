"""
Contains FS related function
"""

import bisect
import json
import os
import re


def get_files(directory, extensions=None):
    """Gets the list of files in a directory and sub-directory

    Args:
        directory (str): path of directory
        extensions (List[str]): list of extensions to search
    """
    directory = os.path.realpath(directory)

    if not os.path.exists(directory):
        raise ValueError('Directory "{}" doesn\'t exist'.format(directory))

    match_ext = "^.+(" + '|'.join(extensions) + ")$" if extensions else None
    count_dirs = 0
    count_files = 0
    count_match_files = 0
    all_files = []
    inc = 0

    for root, _, files in os.walk(directory):
        count_dirs += 1
        if root == directory:
            rel_dir_path = root.replace(directory, './')
            inc = 0
        else:
            rel_dir_path = root.replace(directory, '.')
            inc = 1

        for file in files:
            count_files += 1
            if match_ext is None or re.match(match_ext, file):
                count_match_files += 1
                bisect.insort(
                    all_files, (inc, os.path.join(rel_dir_path, file)))

    print('--all_files', all_files)
    print('--all_files.json', json.dumps(all_files))

    return {
        'files': [f[1] for f in all_files],
        'count_dirs': count_dirs,
        'count_files': count_files,
        'count_match_files': count_match_files,
    }
