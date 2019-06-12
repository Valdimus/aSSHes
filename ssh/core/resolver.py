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


from .cache_daos.cache_dao import CacheDAO

from ..models import User, UserGroup, Host
from ..models import HostGroup, HostTag
from ..models import UnixUser, UnixUserGroup
from ..models import Permission


class Resolver:

    def __init__(self, cache_backend: CacheDAO):
        self.perms = {}
        self.cache_backend = cache_backend

    def add_host(self, fqdn: str):
        if fqdn not in self.perms:
            self.perms[fqdn] = {}

    def add_unix_user(self, fqdn, unix_user):
        self.add_host(fqdn)
        if unix_user not in self.perms[fqdn]:
            self.perms[fqdn][unix_user] = []

    def add_keys(self, fqdn, unix_user, keys):
        self.add_host(fqdn)
        self.add_unix_user(fqdn, unix_user)

        if len(keys) > 0:
            print("On est ici")
            self.perms[fqdn][unix_user] += keys

    def generate_key(self):
        """
        Gerenate key
        :return:
        """

        for perm in Permission.objects.all():
            print(perm)

            hosts = []
            if isinstance(perm.host_target, Host):
                hosts = [perm.host_target.compute_name()]
            elif isinstance(perm.host_target, HostGroup):
                hosts = perm.host_target.unfold_members()
            elif isinstance(perm.host_target, HostTag):
                hosts = [perm.host_target.compute_name()]
            print(hosts)
            for host in hosts:
                for unix_target in perm.unix_target.all():
                    unix_users = []
                    if isinstance(unix_target, UnixUserGroup):
                        unix_users = unix_target.unfold_members()
                    elif isinstance(unix_target, UnixUser):
                        unix_users = [unix_target.name]

                    for unix_user in unix_users:
                        for user_target in perm.user_target.all():
                            keys = []
                            if isinstance(user_target, UserGroup):
                                keys = user_target.unfold_members()
                            elif isinstance(user_target, User):
                                key = user_target.get_key()
                                keys = [key] if key is not None else []
                            print(keys)
                            self.add_keys(host, unix_user, keys)

    def save(self):
        """Save perms on cache system"""
        self.cache_backend.save(self.perms)