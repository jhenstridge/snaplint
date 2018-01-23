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

import os


class Rule:

    def __init__(self, snapinfo):
        # Make sure path ends in a separator to make things easier
        self.info = snapinfo
        self.path = self.info.path

    def get_file_list(self):
        '''Return a list of files in the snap'''
        return self.info.get_file_list()

    def get_dir_list(self):
        '''Return a list of directories in the snap'''
        return self.info.get_dir_list()

    def scan(self):
        '''Override this method to implement your rule checking logic'''
        raise NotImplementedError
