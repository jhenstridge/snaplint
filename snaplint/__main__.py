#!/usr/bin/env python3
#
# Copyright (C) 2016 Canonical, Ltd.
# Author: Scott Sweeny <scott.sweeny@canonical.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import importlib
import pkgutil
import os
import sys
import textwrap

import snaplint
import snaplint.snapinfo
import snaplint.rules

def _snap_path(path):
    if not os.path.exists(path):
        print("%s does not exist" % path)
        return None

    if os.path.exists(os.path.join(path, 'meta', 'snap.yaml')):
        return path
    elif (os.path.exists(os.path.join(path, 'snapcraft.yaml')) or
          os.path.exists(os.path.join(path, '.snapcraft.yaml')) or
          os.path.exists(os.path.join(path, 'snap', 'snapcraft.yaml'))):
        if os.path.exists(os.path.join(path, 'prime', 'meta',
                                       'snap.yaml')):
            return os.path.join(path, 'prime')
        else:
            print("Please run 'snapcraft prime' in your project to"
                  " generate a valid snap directory")
    else:
        print("%s is not a valid snap or snapcraft directory" % path)
        return None

def _parse_args():
    parser = argparse.ArgumentParser(
        description='Clean up your snap',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('project',
                        help=textwrap.dedent('''\
                        snapcraft project directory to test
                        (Should contain snapcraft.yaml)'''))

    args = parser.parse_args()
    return args


def _get_scanner(module):
    for attr in vars(module).values():
        if not isinstance(attr, type):
            continue
        if not issubclass(attr, snaplint.Rule):
            continue
        if attr == snaplint.Rule:
            continue
        return attr

def main():
    args = _parse_args()
    snap = _snap_path(args.project)
    if snap is None:
        print("Please specify a valid snapcraft directory")
        sys.exit(1)

    info = snaplint.snapinfo.SnapInfo(snap)

    # This logic stolen shamelessly from snapcraft

    rules_to_run = []
    for importer, modname, is_package in pkgutil.iter_modules(
            snaplint.rules.__path__):
        rules_to_run.append(modname)

    print('Rules to run: ', rules_to_run)

    print("Running scan")
    fail = False
    for rule in rules_to_run:
        module = None

        try:
            module = importlib.import_module('snaplint.rules.{}'.format(rule))
        except ImportError as ex:
            if ex.name != 'snaplint.rules.{}'.format(rule):
                raise
        if not module:
            print("Cannot find rule {}".format(rule))
            sys.exit(1)
        scanner = _get_scanner(module)
        if not scanner:
            print("Invalid rule: {}".format(rule))
            sys.exit(1)

        scanner_inst = scanner(info)
        if not scanner_inst.scan():
            fail = True

    if fail:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
