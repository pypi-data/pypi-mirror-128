<!--
SPDX-FileCopyrightText: 2021 Joshua Mulliken <joshua@mulliken.net>

SPDX-License-Identifier: GPL-3.0-only
-->

# Red Hat Pastebin CLI Tool

This tool is made to allow Red Hat Employees to quickly and easily upload files to the Red Hat internal Pastebin instance (<https://pastebin.test.redhat.com>).\

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