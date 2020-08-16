import unittest
import json
from utils.file_manager import (get_files)
from .base import (TestFiles, test_data_path)


class TestFileManager(TestFiles, unittest.TestCase):

    def setUp(self):
        self.remove_dir(test_data_path)
        self.create_files(test_data_path)
        self.create_files(test_data_path+'/dir1')
        self.create_files(test_data_path+'/dir2')

    def tearDown(self):
        self.remove_dir(test_data_path)

    def test_get_files_when_dir_exist(self):
        result = get_files(test_data_path)
        self.maxDiff = None
        print('--re', json.dumps(result))
        self.assertDictEqual(result, {'count_dirs': 3,
                                      'count_files': 15,
                                      'count_match_files': 15,
                                      'files': ['./file_01.mp3',
                                                './file_02.mp3',
                                                './file_03.mp3',
                                                './file_04.mp3',
                                                './file_05.mp3',
                                                './dir1/file_01.mp3',
                                                './dir1/file_02.mp3',
                                                './dir1/file_03.mp3',
                                                './dir1/file_04.mp3',
                                                './dir1/file_05.mp3',
                                                './dir2/file_01.mp3',
                                                './dir2/file_02.mp3',
                                                './dir2/file_03.mp3',
                                                './dir2/file_04.mp3',
                                                './dir2/file_05.mp3']})

    def test_get_files_when_dir_missing(self):
        with self.assertRaises(ValueError) as ex:
            get_files('non-existent-path')

        self.assertRegex(str(ex.exception), r'^Directory ".*" doesn\'t exist$')
