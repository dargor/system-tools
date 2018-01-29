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

# https://www.kernel.org/doc/Documentation/sysctl/kernel.txt

REASONS = {
    1: 'A module with a non-GPL (or unknown) license has been loaded.',
    2: 'A module was force loaded by insmod -f.',
    4: 'Unsafe SMP processors: SMP with CPUs not designed for SMP.',
    8: 'A module was forcibly unloaded from the system by rmmod -f.',
    16: 'A hardware machine check error occurred on the system.',
    32: 'A bad page was discovered on the system.',
    64: 'The user has asked that the system be marked "tainted".',
    128: 'The system has died.',
    256: 'The ACPI DSDT has been overridden with one supplied by the user.',
    512: 'A kernel warning has occurred.',
    1024: 'A module from drivers/staging was loaded.',
    2048: 'The system is working around a severe firmware bug.',
    4096: 'An out-of-tree module has been loaded.',
    8192: 'An unsigned module has been loaded.',
    16384: 'A soft lockup has previously occurred on the system.',
    32768: 'The kernel has been live patched.',
}

with open('/proc/sys/kernel/tainted', 'r') as f:
    code = int(f.readline().strip())

print('/proc/sys/kernel/tainted: {}\n'.format(code))

for k, v in REASONS.items():
    if (code ^ k) & k == 0:
        print('{}: {}'.format(k, v))
