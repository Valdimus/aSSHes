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


from ..cache_daos.cache_dao import CacheDAO


class QueryHandler:

    def __init__(self, options: str):
        self.options = options

    @staticmethod
    def extract_parameters(request):
        return request.GET

    def perms(self, request, cache_dao: CacheDAO):
        return self.handle(self.extract_parameters(request), cache_dao)

    def handle(self, parameters: dict, cache_dao: CacheDAO):
        return None
