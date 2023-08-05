#-*- coding:utf-8 -*-
#
# lib/_frozendict.py
#
# This file is part of the NNGT project, a graph-library for standardized and
# and reproducible graph analysis: generate and analyze networks with your
# favorite graph library (graph-tool/igraph/networkx) on any platform, without
# any change to your code.
# Copyright (C) 2015-2021 Tanguy Fardet
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

""" Read-only dict """

class _frozendict(dict):

    def __init__(self, *args, **kwargs):
        self.message = 'Cannot set items of frozendict.'
        if "message" in kwargs:
            self.message = kwargs["message"]
            del kwargs["message"]
        super(_frozendict, self).__init__(*args, **kwargs)

    def __setitem__(self, name, value):
        '''
        Prevent item setting
        '''
        raise RuntimeError(self.message)
