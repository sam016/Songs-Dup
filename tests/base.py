import unittest
import os
import inspect
import pytest
import shutil
import taglib
from utils.file_manager import (get_files)

cur_path = os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda: 0)))
test_mp3_path = os.path.join(cur_path, '1-second-of-silence.mp3')
test_data_path = os.path.join(cur_path, 'data')
def_file_info = [
    # (file_name, artist_name, album_name, song_title)
    ('file_01.mp3', 'artist_01', 'album_01', 'title_01'),
    ('file_02.mp3', 'artist_02', 'album_02', 'title_02'),
    ('file_03.mp3', 'artist_03', 'album_03', 'title_03'),
    ('file_04.mp3', 'artist_01', 'album_01', 'title_01'),
    ('file_05.mp3', 'artist_01', 'album_01', 'title_01'),
]


class TestFiles(unittest.TestCase):

    def create_files(self, dir, files=def_file_info):
        os.makedirs(dir)

        for (file_name, artist_name, album_name, song_title) in files:
            file_path = os.path.join(dir, file_name)
            shutil.copy(test_mp3_path, file_path)

            song = taglib.File(file_path)
            song.tags['ALBUM'] = album_name
            song.tags['ARTIST'] = artist_name
            song.tags['TITLE'] = song_title

            song.save()

    def remove_dir(self, dir):
        if os.path.exists(dir):
            shutil.rmtree(dir)

    def assertFilesShouldExist(self, files):
        if isinstance(files, str):
            return self.assertFilesShouldExist([files])

        if not isinstance(files, list):
            raise AssertionError('arg files should be str or list')

        for file in files:
            self.assertTrue(os.path.exists(file),
                            msg=f'{file} doesn\'t exist')

    def assertFilesShouldNotExist(self, files):
        if isinstance(files, str):
            return self.assertFilesShouldNotExist([files])

        if not isinstance(files, list):
            raise AssertionError('arg files should be str or list')

        for file in files:
            self.assertFalse(os.path.exists(file),
                             msg=f'{file} exists')
