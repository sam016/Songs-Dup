#!/usr/bin/python

import taglib
import argparse
import os
import re
import sys

DEBUG_MODE = False

AUDIO_EXTS = ['mp3']

CLR_END = '\033[00m'
CLR_BOLD = '\033[01m'
CLR_UNDERLINE = '\033[04m'
CLR_RED = '\033[01;91m'
CLR_GREEN = '\033[01;92m'
CLR_YELLOW = '\033[01;93m'
CLR_BLUE = '\033[01;94m'
CLR_PURPLE = '\033[01;95m'
CLR_CYAN = '\033[01;96m'
CLR_DARKCYAN = '\033[01;36m'

CLR_LIGHT_RED = '\033[91m'
CLR_LIGHT_GREEN = '\033[92m'
CLR_LIGHT_YELLOW = '\033[93m'
CLR_LIGHT_BLUE = '\033[94m'
CLR_LIGHT_PURPLE = '\033[95m'
CLR_LIGHT_CYAN = '\033[96m'
CLR_LIGHT_DARKCYAN = '\033[36m'

result = {}


def main():
	params = get_input_params()
	dir_path = params.directory

	str_rubbish = ('|'.join(('(' + re.escape(item) + ')') for item in params.rubbish))

	if not os.path.exists(dir_path):
		print(CLR_LIGHT_RED + 'Directory does not exist')
		sys.exit()

	dir_res = process_directory(dir_path, {'filters':AUDIO_EXTS, 'rubbish':str_rubbish}, process_audio_tag)

	stats = dir_res['stats']
	result = dir_res['result']

	print('Total directories:', stats['count_dirs'])
	print('Total files:', stats['count_files'])
	print('Total audio files:', stats['count_match_files'])

	filter_result(result)
	process_result(result, dir_path)


def get_input_params():
	parser = argparse.ArgumentParser()
	parser.add_argument('directory', help='Path to the directory')
	parser.add_argument('rubbish', help='Rubbish words', nargs='*')
	args = parser.parse_args()

	return args


# filter result to remove the non-repeating items
def filter_result(result):
	keys = [k for k in result.keys()]
	for key in keys:
		if result[key]['count'] <= 1:
			del result[key]


def process_result(result, dir_root):
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
			  (ind_result, count_result, CLR_BOLD, key, count_files, CLR_END))
		print('%s    0 - Skip (Default) %s' % (CLR_RED, CLR_END))

		for file in files:
			print('   %s%2d%s - %s' % (CLR_BLUE, ind_file,
									   CLR_END, file.path.replace(dir_root, '')))
			ind_file += 1

		ind_sel = input(
			"\r\nChoose which file to keep [1 - {0}]:\n> ".format(count_files))

		ind_sel = 0 if ind_sel is '' else ind_sel

		try:
			ind_sel = int(ind_sel)
		except:
			ind_sel = 0

		if ind_sel is 0:
			print('%sSkipping.%s' % (CLR_RED, CLR_END))
		else:
			for it in range(0, count_files):
				if ind_sel == it:
					pass
				else:
					try:
						os.remove(files[it].path)
					except Exception as e:
						print('Error while removing the file.')

		ind_result += 1


def process_directory(directory, options, fx_each_match):
	listfiles = []
	match_ext = "^.+(" + '|'.join(options['filters']) + ")$"
	count_dirs = 0
	count_files = 0
	count_match_files = 0
	options['result'] = {}

	for root, dirs, files in os.walk(directory):
		path = root.split(os.sep)
		count_dirs += 1
		for file in files:
			count_files += 1
			if re.match(match_ext, file):
				count_match_files += 1
				fx_each_match(options, root, file)

	return {'result': options['result'], 'stats': {'count_dirs': count_dirs, 'count_files': count_files, 'count_match_files': count_match_files}}


# cleans the string and array
def clean_item(item, rubbish):
	if item is None:
		return

	if type(item) is str:
		return re.sub(rubbish, '', item).strip()
	elif type(item) is list:
		list_new = []
		for listitem in item:
			list_new.append(clean_item(listitem, rubbish))
		return list_new
	else:
		pass


def process_audio_tag(options, dir, filename):
	path_file = dir + '/' + filename
	file = taglib.File(path_file)
	tags = file.tags
	result = options['result']
	rubbish = options['rubbish']

	if DEBUG_MODE:
		print(filename)

	artist = '?'.join([re.sub(rubbish, '', item).strip() for item in clean_item(
		tags['ARTIST'], rubbish)]) if 'ARTIST' in tags else 'unknown'
	album = '?'.join([re.sub(rubbish, '', item).strip() for item in clean_item(
		tags['ALBUM'], rubbish)]) if 'ALBUM' in tags else 'unknown'
	title = '?'.join([re.sub(rubbish, '', item).strip() for item in clean_item(
		tags['TITLE'], rubbish)]) if 'TITLE' in tags else 'unknown'

	key = artist + '||' + title

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


if __name__ == '__main__':
	main()
	print(CLR_GREEN + 'Finished.')
