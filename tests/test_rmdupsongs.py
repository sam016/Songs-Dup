import unittest
import os
import inspect
import pytest
import shutil
import taglib
from utils.rmdupsongs import (
    process_audio_tag,
    get_tag_count,
    remove_single_tags,
    process_files_result
)

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


class TestFiles:

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
        res = process_audio_tag(os.path.join(test_data_path, 'file_01.mp3'))
        self.assertEqual(res, ('artist_01', 'album_01', 'title_01'))

        res = process_audio_tag(os.path.join(test_data_path, 'file_02.mp3'))
        self.assertEqual(res, ('artist_02', 'album_02', 'title_02'))

        res = process_audio_tag(os.path.join(test_data_path, 'file_05.mp3'))
        self.assertEqual(res, ('artist_01', 'album_01', 'title_01'))

    def test_tag_count_for_files(self):
        files = [
            ('', 'file_01.mp3', os.path.join(test_data_path, 'file_01.mp3')),
            ('', 'file_02.mp3', os.path.join(test_data_path, 'file_02.mp3')),
            ('', 'file_03.mp3', os.path.join(test_data_path, 'file_03.mp3')),
            ('', 'file_04.mp3', os.path.join(test_data_path, 'file_04.mp3')),
            ('', 'file_05.mp3', os.path.join(test_data_path, 'file_05.mp3')),
        ]

        tag_count = get_tag_count(files)

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

        result = remove_single_tags(arg)

        self.assertEqual(result, {
            'artist_01|title_01': {
                'count': 2,
                'files': ['file_01.mp3', 'file_05.mp3'],
                'artist': 'artist_01',
                'album': 'album_01',
                'title': 'title_01'
            }
        })

    def test_process_files_result_dry_run(self):
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

        process_files_result(arg, test_data_path, dry_run=True)

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

        self.assertTrue(os.path.exists(
            os.path.join(test_data_path, 'file_01.mp3')))
        self.assertTrue(os.path.exists(
            os.path.join(test_data_path, 'file_05.mp3')))


if __name__ == '__main__':
    unittest.main()
