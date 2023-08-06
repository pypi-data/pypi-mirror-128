# Treecount Package

[![Setup Automated](https://img.shields.io/badge/setup-automated-blue?logo=gitpod)](https://gitpod.io/from-referrer/)
![Test passing](https://img.shields.io/badge/Tests-passing-brightgreen.svg)
![Python Version](https://img.shields.io/badge/python-3.6+-brightgreen.svg)
[![PyPI version](https://badge.fury.io/py/directory-tree.svg)](https://badge.fury.io/py/directory-tree)
![Last Commit](https://img.shields.io/github/last-commit/rushic24/treecount?style=flat-square)
[![Open Source Love png2](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)


## About 

Ever get confused in counting the number of files in a set of directories? No Worries!

`treecount` is a simple fork of [Directory-tree](https://github.com/rahulbordoloi/Directory-Tree) python utility package that displays out the Tree Structure of a user-defined directory with their respective file count.

<b><i> Currently Available for All Platforms.  </i></b>

## Installation

Run the following command on your terminal to install `treecount`: 

1 .  Installing the package using `pip`:
```python
pip install treecount
```
OR

```python
pip3 install treecount
```

2 . Cloning the repository:

```
git clone https://github.com/rushic24/treecount/
cd Directory-Tree
pip install -e .
```

## Usage

<h4> Arguments </h4>


| __Parameters__ | __Description__ |
|    ---         |       ---       |
| __dir_path__ | Refers to the Directory Path of Operation. By default, refers to the Current Working Directory. |
| __string_rep__ | Refers to whether you just want the direct output or a string representation of the same. |


Run this script in order to print out the tree structure of a user-defined directory!

```python
# Importing Libraries
from treecount import display_tree

# Main Method
if __name__ == '__main__':
    display_tree(directory_path)
```

*   Here by default, the `directory_path` is the current working directory (CWD) unless specified by the user.

## Output

1. For <i>Current Working Directory</i> [DEFAULT] [String Representation = `False`]

```python
>>> from treecount import display_tree
>>> display_tree()

$ Operating System : Windows
$ Path : C:\Personal\Work\Directory-Tree\Test\Main Directory

*************** Directory Tree ***************

Main Directory/
├── Directory 1/
│   └── Directory 2/
│       ├── Directory 3/
│       │   └── Directory 4/
│       │       └── Hello World.txt
│       └── Say World.txt
├── Directory A/
│   └── Hmm.txt
├── directory-tree-print.cpp
├── letseee.txt
└── printTree.exe

```

2. For <i>User Specified Directory</i> [Argument] [String Representation = `True`]

```python
>>> from treecount import display_tree
>>> stringRepresentation = display_tree('C:\Personal\Work\Directory-Tree\Test\Main Directory', string_rep = True)
>>> print(stringRepresentation)

$ Operating System : Windows
$ Path : C:\Personal\Work\Directory-Tree\Test\Main Directory

*************** Directory Tree ***************

Main Directory/
├── Directory 1/
│   └── Directory 2/
│       ├── Directory 3/
│       │   └── Directory 4/
│       │       └── Hello World.txt
│       └── Say World.txt
├── Directory A/
│   └── Hmm.txt
├── directory-tree-print.cpp
├── letseee.txt
└── printTree.exe

```

## Developing `treecount`

To install `treecount`, along with the tools you need to develop and run tests, and execute the following in your virtualenv:

```bash
$ pip install -e .[dev]
```

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://github.com/rushic24/)
