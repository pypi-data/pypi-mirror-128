# generalfile
Easily manage files cross platform.

This package and 6 other make up [ManderaGeneral](https://github.com/ManderaGeneral).

## Information
| Package                                                      | Ver                                            | Latest Release       | Python                                                                                                                   | Platform        |   Lvl | Todo                                                    | Tests   |
|:-------------------------------------------------------------|:-----------------------------------------------|:---------------------|:-------------------------------------------------------------------------------------------------------------------------|:----------------|------:|:--------------------------------------------------------|:--------|
| [generalfile](https://github.com/ManderaGeneral/generalfile) | [2.5.3](https://pypi.org/project/generalfile/) | 2021-11-19 18:47 CET | [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/) | Windows, Ubuntu |     1 | [3](https://github.com/ManderaGeneral/generalfile#Todo) | 100.0 % |

## Contents
<pre>
<a href='#generalfile'>generalfile</a>
├─ <a href='#Information'>Information</a>
├─ <a href='#Contents'>Contents</a>
├─ <a href='#Installation'>Installation</a>
├─ <a href='#Attributes'>Attributes</a>
└─ <a href='#Todo'>Todo</a>
</pre>

## Installation
| Command                   | <a href='https://pypi.org/project/generallibrary'>generallibrary</a>   | <a href='https://pypi.org/project/send2trash'>send2trash</a>   | <a href='https://pypi.org/project/appdirs'>appdirs</a>   | <a href='https://pypi.org/project/pandas'>pandas</a>   | <a href='https://pypi.org/project/dill'>dill</a>   |
|:--------------------------|:-----------------------------------------------------------------------|:---------------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------------|:---------------------------------------------------|
| `pip install generalfile` | Yes                                                                    | Yes                                                            | Yes                                                      | Yes                                                    | Yes                                                |

## Attributes
<pre>
<a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/__init__.py#L1'>Module: generalfile</a>
├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/errors.py#L1'>Class: CaseSensitivityError</a>
├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/errors.py#L1'>Class: InvalidCharacterError</a>
└─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path.py#L1'>Class: Path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path.py#L1'>Class: Path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: absolute</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_lock.py#L1'>Method: as_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/optional_dependencies/path_cfg.py#L1'>Property: cfg</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: contains</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: copy</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: copy_to_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: create_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: delete</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: delete_folder_content</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: empty</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: encode</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: endswith</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: exists</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: from_alternative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: get_cache_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: get_differing_files</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: get_lock_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: get_lock_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: get_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: is_absolute</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: is_file</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: is_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: is_identical</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: is_relative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: is_root</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_lock.py#L1'>Method: lock</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: match</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: mirror_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: move</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: name</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: open_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: open_operation</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: pack</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: parts</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/optional_dependencies/path_pickle.py#L1'>Property: pickle</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: read</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: relative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: remove_end</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: remove_start</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: rename</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: same_destination</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path.py#L1'>Method: scrub</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: seconds_since_creation</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: seconds_since_modified</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: set_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: size</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/optional_dependencies/path_spreadsheet.py#L1'>Property: spreadsheet</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: startswith</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: suffix</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: suffixes</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/optional_dependencies/path_text.py#L1'>Property: text</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: to_alternative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: trash</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: trash_folder_content</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: true_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: unpack</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: with_name</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: with_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: with_suffix</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: with_suffixes</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_strings.py#L1'>Method: with_true_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: without_file</a>
   └─ <a href='https://github.com/ManderaGeneral/generalfile/blob/0d923a0/generalfile/path_operations.py#L1'>Method: write</a>
</pre>

## Todo
| Module                                                                                                                                               | Message                                                                                                                                                                                   |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/optional_dependencies/path_spreadsheet.py#L1'>path_spreadsheet.py</a> | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/optional_dependencies/path_spreadsheet.py#L112'>Support DataFrame and Series with spreadsheet.append()</a> |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path_lock.py#L1'>path_lock.py</a>                                     | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path_lock.py#L12'>Lock the optional extra paths.</a>                                                       |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L1'>path.py</a>                                               | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L23'>Binary extension.</a>                                                                         |

<sup>
Generated 2021-11-19 18:47 CET for commit <a href='https://github.com/ManderaGeneral/generalfile/commit/0d923a0'>0d923a0</a>.
</sup>
