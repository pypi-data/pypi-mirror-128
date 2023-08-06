#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-only

import argparse
import requests
import sys


def paste_text(text, expiry='m', text_style='text'):
    # Expiry options: f = Forever, m = Month, d = Day
    # Text style options: text = Plain text, html = HTML, bash = Bash, python = Python
    data = {
        'parent_pid': '',
        'format': text_style,
        'code2': text,
        'poster': '',
        'expiry': expiry,
        'paste': 'Send'
    }

    paste_id_res = requests.post('http://pastebin.test.redhat.com/pastebin.php', data)
    if paste_id_res.status_code == 200:
        paste_url = paste_id_res.url
        return paste_url
    else:
        raise Exception('Error: {}'.format(paste_id_res.status_code))


def cli():
    parser = argparse.ArgumentParser(description='Tool to upload text content from the cli to pastebin.test.redhat.com.')
    parser.add_argument('-f', '--format', help='format of text (default: text): text, html, bash, python...', required=False)
    parser.add_argument('-e', '--expiry', help='expiry of paste (default: m): f = Forever, m = Month, d = Day', required=False)

    args = parser.parse_args()

    if not sys.stdin.isatty():
        text = sys.stdin.read()
        text_style = 'text'
        if args.format:
            text_style = args.format
        expiry = 'm'
        if args.expiry:
            expiry = args.expiry

        paste_id = paste_text(text, text_style=text_style, expiry=expiry)
        print(paste_id)
    else:
        print("Error: no text found in stdin.")

if __name__ == '__main__':
    cli()
