#! /usr/bin/env python3
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

from glob import glob


def read_stuff(fname):

    with open(fname, 'r') as fd:
        data = fd.readlines()
    assert len(data) == 1

    return data[0].strip()


for fname in glob('/proc/[0-9]*/oom_adj'):

    # Values of oom_adj :
    #   -17 = immune to oom killer
    #   -16 = very unlikely to be killed
    #   ...
    #   +15 = very likely to be killed

    oom_adj = int(read_stuff(fname))
    if oom_adj >= 0:
        continue

    cmdline = read_stuff(fname.replace('oom_adj', 'cmdline')).split('\0')[0]

    print(f'{cmdline} -> {oom_adj}')
