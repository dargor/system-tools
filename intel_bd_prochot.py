#! /usr/bin/env python
#
# Copyright (c) 2018, Gabriel Linder <linder.gabriel@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from argparse import ArgumentParser

import subprocess


parser = ArgumentParser()

parser.add_argument('-v',
                    '--verbose',
                    help='Print commands before running them',
                    action='store_true',
                    required=False)

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('-s',
                   '--status',
                   help='Show BD PROCHOT status',
                   action='store_true',
                   required=False)

group.add_argument('-e',
                   '--enable',
                   help='Enable BD PROCHOT',
                   action='store_true',
                   required=False)

group.add_argument('-d',
                   '--disable',
                   help='Disable BD PROCHOT',
                   action='store_true',
                   required=False)

args = parser.parse_args()


def run(cmd):
    try:
        if args.verbose:
            print('[90m>>> {}[0m'.format(' '.join(cmd)))
        return subprocess.check_output(cmd).decode().strip()
    except Exception as e:
        print('Error: {}'.format(e))
        print('Hint: Are msr-tools installed ?')
        print('Hint: Are you running as root ?')
        exit(1)


def status(step):
    status = int(run(['rdmsr', '0x1fc', '--bitfield', '0:0'])) == 1
    if status:
        print('BD PROCHOT is {} [91menabled[0m.'.format(step))
    else:
        print('BD PROCHOT is {} [92mdisabled[0m.'.format(step))
    return status


if args.status:
    status('currently')
    exit(0)


msr = [int(x, 16) for x in run(['rdmsr', '-xa', '0x1fc']).split('\n')]
print('Current msr: {}'.format([hex(x) for x in msr]))

if args.enable:
    if status('currently'):
        print('BD PROCHOT is already enabled.')
        exit(0)
    print('\nTrying to enable BD PROCHOT')
    msr = [x + 1 for x in msr]

if args.disable:
    if not status('currently'):
        print('BD PROCHOT is already disabled.')
        exit(0)
    print('\nTrying to disable BD PROCHOT')
    msr = [x - 1 for x in msr]

print('Setting msr to: {}'.format([hex(x) for x in msr]))
run(['wrmsr', '-a', '0x1fc', str(msr[0])])

status('now')
