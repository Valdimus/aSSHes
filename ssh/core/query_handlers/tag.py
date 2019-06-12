# coding: utf-8

# Copyright (C) 2019 NOUCHET Christophe
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

# Author: Christophe Nouchet
# Email: nouchet.christophe@gmail.com
# Date: 2019


import json
from .query_handler import QueryHandler

from ..cache_daos.cache_dao import CacheDAO


class TagQueryHandler(QueryHandler):

    def compute_option(self):
        return json.loads(self.options)

    def compute_name(self, tags, parameters):
        return "-".join([
            "%s:%s" % (tag, parameters[tag])
            for tag in tags
        ])

    def handle(self, parameters: dict, cache_dao: CacheDAO):
        tags_to_test = sorted(self.compute_option())

        for tag_to_test in tags_to_test:
            if tag_to_test not in parameters:
                return None

        print(self.compute_name(tags_to_test, parameters))
        return cache_dao.get_perms(self.compute_name(tags_to_test, parameters))
