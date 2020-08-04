# Songs-Dup

1. [Introduction](#1-introduction)
1. [Requirements](#2-requirements)
1. [How to use](#3-how-to-use)


## 1. Introduction

A python script which deletes duplicate songs in a directory by reading thier meta information.

## 2. Requirements

- Install [Python 3](https://www.python.org/downloads/)
- Install [pytaglib](https://pypi.python.org/pypi/pytaglib) dependencies from here: https://github.com/supermihi/pytaglib#installation-notes
- Install the requirements
  - [pytaglib](https://pypi.python.org/pypi/pytaglib)

Following is a quick way to install dependencies:
```
    pip install -r requirements.txt
```

## 3. How to use

`python rmdupsongs.py directory_path`


	usage: rmdupsongs.py [-h] [--rubbish [RUBBISH [RUBBISH ...]]] directory

	Removes duplicate songs by reading the meta tags

	positional arguments:
	  directory             Path to the directory

	optional arguments:
	  -h, --help            show this help message and exit
	  --rubbish [RUBBISH [RUBBISH ...]]
	                        Rubbish words
