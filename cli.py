import argparse
import os
import sys
from utils import remove_dup_songs
from colorama import init, Fore


def main():
    """Main driver
    """
    params = get_input_params()
    dir_path = params.directory

    remove_dup_songs(dir_path, params)


def get_input_params():
    """Get the input params from cli arguments
    """
    parser = argparse.ArgumentParser(
        description='Removes duplicate songs by reading the meta tags')
    parser.add_argument('directory', help='Path to the directory')
    parser.add_argument('--rubbish', help='Rubbish words', nargs='*')
    parser.add_argument(
        '--dry-run', help='Dry runs the execution without affecting actual files', default=False, dest='dry_run')
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    init(autoreset=True)
    main()
    print(Fore.GREEN + 'Finished deleting duplicate songs, enjoy your music :)')
