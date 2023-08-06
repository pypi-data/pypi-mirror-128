<!--
SPDX-FileCopyrightText: 2021 Joshua Mulliken <joshua@mulliken.net>

SPDX-License-Identifier: GPL-3.0-only
-->

# Red Hat Pastebin CLI Tool

This tool is made to allow Red Hat Employees to quickly and easily upload files to the Red Hat internal Pastebin instance (<https://pastebin.test.redhat.com>).

## Instructions

Install with pip

```bash
$ pip3 install rhpaste
```


Usage:

```bash
$ cat myfile.txt | rhpaste
http://pastebin.test.redhat.com/xxxxxxx
```

Expanded usage:

```bash
$ rhpaste --help
usage: rhpaste [-h] [-f FORMAT] [-e EXPIRY]

Tool to upload text content from the cli to pastebin.test.redhat.com.

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        format of text: text, html, bash, python...
  -e EXPIRY, --expiry EXPIRY
                        expiry of paste: f = Forever, m = Month, d = Day
```