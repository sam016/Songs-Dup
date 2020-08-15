import unittest
import os
import inspect
import pytest
import shutil
import taglib
from .base import (TestFiles, test_data_path)
from utils.song_manager import SongManager


class TestWhenFilesArePresent(TestFiles, unittest.TestCase):

    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        self.remove_dir(test_data_path)
        self.create_files(test_data_path)
        self.create_files(test_data_path+'/dir1')
        self.create_files(test_data_path+'/dir2')

    def tearDown(self):
        self.remove_dir(test_data_path)

    def test_process_audio_tag(self):
        song_manager = SongManager()

        res = song_manager.__process_audio_tag__(
            os.path.join(test_data_path, 'file_01.mp3'))
        self.assertEqual(res, ('artist_01', 'album_01', 'title_01'))

        res = song_manager.__process_audio_tag__(
            os.path.join(test_data_path, 'file_02.mp3'))
        self.assertEqual(res, ('artist_02', 'album_02', 'title_02'))

        res = song_manager.__process_audio_tag__(
            os.path.join(test_data_path, 'file_05.mp3'))
        self.assertEqual(res, ('artist_01', 'album_01', 'title_01'))

    def test_tag_count_for_files(self):
        song_manager = SongManager()

        files = [
            ('', 'file_01.mp3', os.path.join(test_data_path, 'file_01.mp3')),
            ('', 'file_02.mp3', os.path.join(test_data_path, 'file_02.mp3')),
            ('', 'file_03.mp3', os.path.join(test_data_path, 'file_03.mp3')),
            ('', 'file_04.mp3', os.path.join(test_data_path, 'file_04.mp3')),
            ('', 'file_05.mp3', os.path.join(test_data_path, 'file_05.mp3')),
        ]

        tag_count = song_manager.__get_tag_count__(files)

        self.assertEqual(tag_count, {
            'artist_01|title_01': {
                'count': 3,
                'files': ['file_01.mp3', 'file_04.mp3', 'file_05.mp3'],
                'artist': 'artist_01',
                'album': 'album_01',
                'title': 'title_01'
            },
            'artist_02|title_02': {
                'count': 1,
                'files': ['file_02.mp3'],
                'artist': 'artist_02',
                'album': 'album_02',
                'title': 'title_02'
            },
            'artist_03|title_03': {
                'count': 1,
                'files': ['file_03.mp3'],
                'artist': 'artist_03',
                'album': 'album_03',
                'title': 'title_03'
            }
        })

    def test_remove_single_tags(self):
        song_manager = SongManager()

        arg = {
            'artist_01|title_01': {
                'count': 2,
                'files': ['file_01.mp3', 'file_05.mp3'],
                'artist': 'artist_01',
                'album': 'album_01',
                'title': 'title_01'
            },
            'artist_02|title_02': {
                'count': 1,
                'files': ['file_02.mp3'],
                'artist': 'artist_02',
                'album': 'album_02',
                'title': 'title_02'
            }
        }

        result = song_manager.__remove_single_tags__(arg)

        self.assertEqual(result, {
            'artist_01|title_01': {
                'count': 2,
                'files': ['file_01.mp3', 'file_05.mp3'],
                'artist': 'artist_01',
                'album': 'album_01',
                'title': 'title_01'
            }
        })

    def test_process_files_result_should_not_delete_if_dry_run(self):
        song_manager = SongManager()

        arg = {
            'artist_01|title_01': {
                'count': 2,
                'files': ['file_01.mp3', 'file_05.mp3'],
                'artist': 'artist_01',
                'album': 'album_01',
                'title': 'title_01'
            }
        }

        os.environ['COLORED'] = 'False'

        song_manager.__process_files_result__(
            arg, test_data_path, dry_run=True)

        out, err = self.capsys.readouterr()

        self.assertEqual(err, '')
        self.assertEqual(out, "\n" +
                         "1/1 - artist_01|title_01 [2]\n" +
                         "\n" +
                         "    0 - Skip (Default)\n" +
                         "    1 - file_01.mp3\n" +
                         "    2 - file_05.mp3\n" +
                         "\n" +
                         "    DRY-RUN: skipping\n")

        self.assertFilesShouldExist([
            os.path.join(test_data_path, 'file_01.mp3'),
            os.path.join(test_data_path, 'file_05.mp3'),
        ])

    def test_process_files_result_should_be_deleted(self):
        song_manager = SongManager()

        arg = {
            'artist_01|title_01': {
                'count': 2,
                'files': ['file_01.mp3', 'file_05.mp3'],
                'artist': 'artist_01',
                'album': 'album_01',
                'title': 'title_01'
            }
        }

        os.environ['COLORED'] = 'False'

        song_manager.input = lambda x: '2'
        song_manager.__process_files_result__(arg, test_data_path)

        self.assertFilesShouldExist(
            os.path.join(test_data_path, 'file_01.mp3'))
        self.assertFilesShouldNotExist(
            os.path.join(test_data_path, 'file_05.mp3'))


if __name__ == '__main__':
    unittest.main()
