
import argparse
import os
import re
import sys

from colorama import Fore, Style
import taglib

from .file_manager import get_files

DEBUG_MODE = False

AUDIO_EXTS = ['mp3']

def remove_dup_songs(dir_path, params):
    if not os.path.exists(dir_path):
        print(Fore.LIGHTRED_EX + 'Directory does not exist')
        sys.exit()

    files, count_dirs, count_files, count_match_files = get_files(
        dir_path, extensions=AUDIO_EXTS)

    print('Total directories:', count_dirs)
    print('Total files:', count_files)
    print('Total audio files:', count_match_files)

    # gets the count of artist-title from list of files
    result = get_tag_count(files, rubbish=params.rubbish)

    # removes the non-repeating tags from result
    result = remove_single_tags(result)

    process_files_result(result, dir_path, dry_run=params.dry_run)


def remove_single_tags(result):
    """cleans result: removes the non-repeating items
    """
    keys = [k for k in result.keys()]
    for key in keys:
        if result[key]['count'] <= 1:
            del result[key]

    return result


def process_files_result(result, dir_root, dry_run=False):
    sorted_result = sorted(result, key=(
        lambda key: result[key]['count']), reverse=True)
    ind_result = 1
    count_result = len(sorted_result)

    for key in sorted_result:
        ind_file = 1
        ind_sel = 1
        files = result[key]['files']
        count_files = result[key]['count']

        print('\r\n%d/%d - %s%s:%d%s\r\n' %
              (ind_result, count_result, Fore.MAGENTA, key, count_files, Fore.RESET))
        print('%s    0 - Skip (Default) %s' % (Fore.RED, Fore.RESET))

        for file in files:
            print('   %s%2d%s - %s' % (Fore.BLUE, ind_file,
                                       Fore.RESET, file.path.replace(dir_root, '')))
            ind_file += 1

        if dry_run:
            ind_sel = 0
            print('DRY-RUN: skipping')
        else:
            ind_sel = input(
                "\r\nChoose which file to keep [1 - {0}]:\n> ".format(count_files))

        ind_sel = 0 if ind_sel == '' else ind_sel

        try:
            ind_sel = int(ind_sel)
        except:
            ind_sel = 0

        if ind_sel == 0:
            print('%sSkipping.%s' % (Fore.RED, Fore.RESET))
        else:
            for ind in range(0, count_files):
                if ind_sel == ind:
                    pass
                else:
                    try:
                        os.remove(files[ind].path)
                    except Exception as e:
                        print('Error while removing the file.')

        ind_result += 1


def get_tag_count(files, rubbish=None):
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
    for (_, file, file_path) in files:
        artist, album, title = process_audio_tag(
            file_path, rubbish=str_rubbish)

        key = get_key(artist, album, title)

        if key in result:
            result[key]['count'] += 1
            result[key]['files'].append(file)
        else:
            result[key] = {
                'count': 1,
                'files': [file],
                'artist': artist,
                'album': album,
                'title': title,
            }

    return result


# cleans the string and array
def clean_item(item, rubbish):
    if item is None:
        return None

    if isinstance(item, str):
        return re.sub(rubbish, '', item).strip()

    if isinstance(item, list):
        list_new = []
        for listitem in item:
            list_new.append(clean_item(listitem, rubbish))
        return list_new

    return None


def get_key(artist, album, title):
    return artist + '|' + title


def process_audio_tag(file_path, rubbish=''):
    """Process audio tags for a mp3 file
    """

    if not os.path.exists(file_path):
        raise ValueError('File not found: "%s"' % (file_path))

    # path_file = os.path.join(dir, filename)
    file = taglib.File(file_path)
    tags = file.tags

    if DEBUG_MODE:
        print(file_path)

    artist = '?'.join([re.sub(rubbish, '', item).strip() for item in clean_item(
        tags['ARTIST'], rubbish)]) if 'ARTIST' in tags else 'unknown'
    album = '?'.join([re.sub(rubbish, '', item).strip() for item in clean_item(
        tags['ALBUM'], rubbish)]) if 'ALBUM' in tags else 'unknown'
    title = '?'.join([re.sub(rubbish, '', item).strip() for item in clean_item(
        tags['TITLE'], rubbish)]) if 'TITLE' in tags else 'unknown'

    return (artist, album, title)
