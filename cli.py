"""
main cli.py

    usage: cli.py [-h] [--rubbish [RUBBISH [RUBBISH ...]]] [--dry-run] directory

    Removes duplicate songs by reading the meta tags

    positional arguments:
    directory             Path to the directory

    optional arguments:
    -h, --help            show this help message and exit
    --rubbish [RUBBISH [RUBBISH ...]]
                          Rubbish words in artist name or song title
    --dry-run             Dry runs the execution without affecting actual files

"""

import argparse
from colorama import init, Fore
from utils import SongManager


def main():
    """Main driver
    """
    params = get_input_params()
    dir_path = params.directory

    song_manager = SongManager()

    song_manager.remove_dup_songs(dir_path, params)


def get_input_params():
    """Get the input params from cli arguments
    """
    parser = argparse.ArgumentParser(
        description='Removes duplicate songs by reading the meta tags')
    parser.add_argument('directory', help='Path to the directory')
    parser.add_argument('--rubbish', help='Rubbish words', nargs='*')
    parser.add_argument(
        '--dry-run',
        help='Dry runs the execution without affecting actual files',
        default=False,
        action='store_true',
        dest='dry_run')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    init(autoreset=True)
    main()
    print(Fore.GREEN + 'Finished deleting duplicate songs, enjoy your music :)')
