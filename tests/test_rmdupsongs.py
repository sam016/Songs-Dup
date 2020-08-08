import unittest
import os
import inspect
import shutil
import taglib
from utils.rmdupsongs import process_audio_tag

cur_path = os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda: 0)))
test_mp3_path = os.path.join(cur_path, '1-second-of-silence.mp3')
test_data_path = os.path.join(cur_path, 'data')
def_file_info = [
    # (file_name, artist_name, album_name, song_title)
    ('file_01.mp3', 'artist_01', 'album_01', 'title_01'),
    ('file_02.mp3', 'artist_02', 'album_02', 'title_02'),
    ('file_03.mp3', 'artist_03', 'album_03', 'title_03'),
    ('file_04.mp3', 'artist_04', 'album_04', 'title_04'),
    ('file_05.mp3', 'artist_05', 'album_05', 'title_05'),
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

    def remove_dir(self, dir):
        if os.path.exists(dir):
            shutil.rmtree(dir)


class TestWhenFilesArePresent(TestFiles, unittest.TestCase):

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        self.remove_dir(test_data_path)
        self.create_files(test_data_path)
        self.create_files(test_data_path+'/dir1')
        self.create_files(test_data_path+'/dir2')

    def tearDown(self):
        self.remove_dir(test_data_path)

    def test_audio_tags(self):
        res = process_audio_tag(os.path.join(test_data_path, 'file_01.mp3'))


if __name__ == '__main__':
    unittest.main()
