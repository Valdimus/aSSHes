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


import time
import json

from redis import Redis
from redis.exceptions import ConnectionError

from .cache_dao import CacheDAO


class RedisBackend(CacheDAO):

    def __init__(self, redis1: Redis, redis2: Redis):
        self.redis1 = redis1
        self.redis2 = redis2

    @staticmethod
    def __test_dabase(redis: Redis):
        """Test database"""
        if redis is None:
            return False
        try:
            redis.get("last_updated")
            return True
        except ConnectionError:
            return False

    @staticmethod
    def __get_last_updated(redis: Redis):
        """Get the last time the redis was updated"""
        temp = redis.get("last_updated")
        return float(temp.decode()) if temp else 0

    def active_database(self):
        """Get the active database"""
        redis_test_1 = self.__test_dabase(self.redis1)
        redis_test_2 = self.__test_dabase(self.redis2)
        if redis_test_1 and redis_test_2:
            temp1 = self.__get_last_updated(self.redis1)
            temp2 = self.__get_last_updated(self.redis2)

            if temp1 >= temp2:
                return self.redis1
            else:
                return self.redis2
        elif redis_test_1:
            return self.redis1
        elif redis_test_2:
            return self.redis2

    def inactive_database(self):
        """Get the inactive database"""
        active_database = self.active_database()

        if active_database == self.redis2 and self.__test_dabase(self.redis1):
            return self.redis1
        elif active_database == self.redis1 and self.__test_dabase(self.redis2):
            return self.redis2
        else:
            return active_database

    def save(self, perms: dict):
        """Save perms on cache"""

        redis = self.inactive_database()

        # Clean database
        redis.flushdb()

        redis.hmset("perms", {
            hostname: json.dumps(keys)
            for hostname, keys in perms.items()
        })

        # Changement de redis
        redis.set("last_updated", time.time())

    def get_perms(self, hostname: str=None):
        if hostname is None:
            return self.active_database().hgetall("perms")
        else:
            return self.active_database().hget("perms", hostname)