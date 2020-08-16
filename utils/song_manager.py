
import os
import re

import taglib

from .file_manager import get_files
from .cprint import cprint

DEBUG_MODE = False

AUDIO_EXTS = ['mp3']


class SongManager:
    input = None

    def remove_dup_songs(self, dir_path, params):
        if not os.path.exists(dir_path):
            cprint('Directory "{}" does not exist'.format(dir_path), color='red')
            return

        files_result = get_files(dir_path, extensions=AUDIO_EXTS)

        print('Total directories:', files_result['count_dirs'])
        print('Total files:', files_result['count_files'])
        print('Total audio files:', files_result['count_match_files'])

        # gets the count of artist-title from list of files
        result = self.__get_tag_count__(dir_path,
                                        files_result['files'],
                                        rubbish=params.rubbish)

        # removes the non-repeating tags from result
        result = SongManager.__remove_single_tags__(result)

        self.__process_files_result__(result, dir_path, dry_run=params.dry_run)

    @staticmethod
    def __remove_single_tags__(result):
        """cleans result: removes the non-repeating items
        """
        keys = [k for k in result.keys()]
        for key in keys:
            if result[key]['count'] <= 1:
                del result[key]

        return result

    def __process_files_result__(self, result, dir_root, dry_run=False):
        tmp_input = self.input if self.input else input
        sorted_result = sorted(result, key=(
            lambda key: (result[key]['count'], key)), reverse=True)
        ind_result = 1
        count_result = len(sorted_result)

        for key in sorted_result:
            ind_file = 1
            ind_sel = 1
            files = result[key]['files']
            count_files = result[key]['count']

            print('\n%d/%d' % (ind_result, count_result), end=' - ')
            cprint('%s [%d]\n' % (key, count_files), color='magenta')
            cprint('    0 - Skip (Default)', color='red')

            for file in files:
                cprint('   %2d' % (ind_file), color='blue', end=' - ')
                cprint('%2s' % file)
                ind_file += 1

            if dry_run:
                cprint('\n    DRY-RUN: skipping', color='yellow')
                continue

            ind_sel = tmp_input(
                "\nChoose which file to keep [1 - {0}]:\n> ".format(count_files))

            ind_sel = 0 if ind_sel == '' else ind_sel

            try:
                ind_sel = int(ind_sel)
            except ValueError:
                ind_sel = 0

            if ind_sel == 0:
                cprint('Skipping.', color='red')
            else:
                ind_sel -= 1
                for ind in range(0, count_files):

                    # keep the selected file
                    if ind == ind_sel:
                        continue

                    # remove other files
                    try:
                        os.remove(os.path.join(dir_root, files[ind]))
                    except Exception as e:
                        print('Error while removing the file.', e)

            ind_result += 1

    def __get_tag_count__(self, dir_path, files, rubbish=None):
        """Processes mp3 files and prepares count of artists with their titles
        """

        result = {}

        # prepares regex for rubbish words
        if rubbish is not None:
            str_rubbish = ('|'.join(('(' + re.escape(item) + ')')
                                    for item in rubbish))
        else:
            str_rubbish = ''

        # iterate thru each mp3 file
        for file_path in files:
            artist, album, title = self.__process_audio_tag__(dir_path,
                                                              file_path, rubbish=str_rubbish)

            key = SongManager.__get_key__(artist, title)

            if key in result:
                result[key]['count'] += 1
                result[key]['files'].append(file_path)
            else:
                result[key] = {
                    'count': 1,
                    'files': [file_path],
                    'artist': artist,
                    'album': album,
                    'title': title,
                }

        return result

    # cleans the string and array

    def __clean_item__(self, item, rubbish):
        if item is None:
            return None

        if isinstance(item, str):
            return re.sub(rubbish, '', item).strip()

        if isinstance(item, list):
            list_new = []
            for listitem in item:
                list_new.append(self.__clean_item__(listitem, rubbish))
            return list_new

        return None

    @staticmethod
    def __get_key__(artist, title):
        return artist + '|' + title

    def __process_audio_tag__(self, dir_path, file_path, rubbish=''):
        """Process audio tags for a mp3 file
        """

        full_path = os.path.join(dir_path, file_path)

        if not os.path.exists(full_path):
            raise ValueError('File not found: "%s"' % (full_path))

        file = taglib.File(full_path)
        tags = file.tags

        if DEBUG_MODE:
            print(full_path)

        artist = '?'.join([re.sub(rubbish, '', item).strip() for item in self.__clean_item__(
            tags['ARTIST'], rubbish)]) if 'ARTIST' in tags else 'unknown'
        album = '?'.join([re.sub(rubbish, '', item).strip() for item in self.__clean_item__(
            tags['ALBUM'], rubbish)]) if 'ALBUM' in tags else 'unknown'
        title = '?'.join([re.sub(rubbish, '', item).strip() for item in self.__clean_item__(
            tags['TITLE'], rubbish)]) if 'TITLE' in tags else 'unknown'

        return (artist, album, title)
