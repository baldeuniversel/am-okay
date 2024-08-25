
# Documentation for `am-okay` (version 3.1.2)

## Table of Contents

1. [Introduction](#introduction)
2. [Overview](#overview)
3. [Requirements](#requirements)
4. [Synopsis](#synopsis)
5. [Options](#options)
6. [Usage Examples](#usage-examples)
7. [Notes](#notes)
8. [Author and Contributors](#author-and-contributors)

## Introduction

`am-okay` is a command-line program designed to dynamically copy, cut, and paste files or directories across different terminal sessions. This functionality allows users to initiate a file operation in one terminal session and complete it in another, as long as both sessions are under the same user profile.

## Overview

`am-okay` supports a variety of options to manage files and directories effectively. These options provide users with the flexibility to copy, cut, and paste files or directories, either directly or through indexed actions. The program is inspired by Ve-Quantic principles, providing a robust and dynamic file management experience.

## Requirements

To use `am-okay`, the following preconditions must be met:

- The program requires at least one option to be specified.
- If an index is used (via `--index` or `-i`), it must be a positive integer between 0 and 3.
- Certain options are interdependent (e.g., `--paste-copy` must follow a `--copy` action).
- File or directory names must not contain the character `?`.

## Synopsis

```
am-okay [option | options] [target-dirs | target-files]
```

## Options

- `--copy`, `-c`  
  Copies the specified file(s) or directory(ies). You can use the wildcard `*` to target all contents in the current directory.  
  **Example:** `am-okay --copy <target-dir-or-file>`

- `--cut`, `-x`   
  Cuts the specified file(s) or directory(ies). The wildcard `*` can be used similarly as with the `--copy` option.  
  **Example:** `am-okay --cut <target-dir-or-file>`

- `--paste-copy`, `--paste-c`, `-pc`  
  Pastes files or directories that were previously copied. This must follow a `--copy` action.  
  **Example:** `am-okay --paste-copy <target-directory>`

- `--paste-cut`, `--paste-x`, `-px`  
  Pastes files or directories that were previously cut. This must follow a `--cut` action.  
  **Example:** `am-okay --paste-cut <target-directory>`

- `--array`, `-a`  
  Allows multiple copy or cut actions to be indexed for later use.  
  **Example:** `am-okay --array --index 0 --copy <file-1> <dir-1>`

- `--index`, `-i`   
  Specifies the index for `--array` actions.  
  **Example:** `am-okay --array --index 0 --copy <file-1>`

- `--put`, `-p`  
  Puts files or directories stored in an array index to a target location.  
  **Example:** `am-okay --array --index 0 --put <target-dir>`

- `--stat-copy`, `--stat-c`, `-sc`  
  Displays the status of the last copy action.  
  **Example:** `am-okay --stat-copy`

- `--stat-cut`, `--stat-x`, `-sx`   
  Displays the status of the last cut action.  
  **Example:** `am-okay --stat-cut`

- `--stat`, `-s`  
  Displays the status of an action associated with `--array`.  
  **Example:** `am-okay --array --index 0 --stat`

- `--out`, `-o`  
  Specifies the output directory for direct actions like `--copy` or `--cut`.  
  **Example:** `am-okay --copy <target> --out <output-dir>`

- `--reset`, `-r`   
  Resets all actions. The word `request` must follow this option.  
  **Example:** `am-okay --reset request`

- `--doc`  
  Displays the documentation for the `am-okay` program.  
  **Example:** `am-okay --doc`

- `--help`   
  Displays help information.  
  **Example:** `am-okay --help`

- `--version`  
  Displays the current version of `am-okay`.  
  **Example:** `am-okay --version`

## Usage Examples

1. **Copy a directory**  
   ```bash
   am-okay --copy /path/to/directory
   ```

2. **Cut a file and paste it into another directory**  
   ```bash
   am-okay --cut /path/to/file
   am-okay --paste-cut /path/to/destination
   ```

3. **Using array and indexes to manage multiple operations**  
   ```bash
   am-okay --array --index 0 --copy /path/to/file1
   am-okay --array --index 1 --cut /path/to/file2
   am-okay --array --index 0 --put /destination/for/file1
   ```

4. **Check the status of a copy operation**  
   ```bash
   am-okay --stat-copy
   ```

## Notes

- `am-okay` relies on certain programs that are required as part of its global package.
- Actions performed with the `--copy` option can be repeated using the `--paste-copy` option without re-initiating the copy.
- Similarly, actions performed with the `--cut` option can be repeated using the `--paste-cut` option.
- The `--copy` and `--cut` options have different hash codes and thus manage different sets of files or directories.
- The program operates based on the user profile under which it is run. To ensure consistent operations, use the same profile for all related actions.
- A progress bar will display during copy or move operations executed with `--paste-copy`, `--paste-cut`, or `--put`.

## Author and Contributors

- **Author**: Baldé Amadou - [baldeuniversel@protonmail.com](mailto:baldeuniversel@protonmail.com)
- **Contributor**: Diallo Ismaila - [diallois@protonmail.com](mailto:diallois@protonmail.com)

**Feel free to reach out to the author for any queries or contributions related to the `am-okay` program**.

---

This documentation provides a comprehensive overview and should help in effectively utilizing the `am-okay` program.
