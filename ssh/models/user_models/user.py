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

"""Definition of User"""

from django.db import models

from .user_base import UserBase


class User(UserBase):
    """User to serve ssh public key"""
    login = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    creation_date = models.DateTimeField('Creation date')
    revoked = models.BooleanField(default=False)

    def __str__(self):
        return self.login

    def host_access(self):
        """Get hosts that the user have access"""
        perms = []
        for perm in self.user_target.all():
            perms.append(perm.user_access())

        for user_group in self.members.all():
            for perm in user_group.user_target.all():
                if perm not in perms:
                    perms.append((perm.user_access()))
        return perms

    def get_key(self):
        """Get the active key"""
        # return self.sshkey_set.filter()
        key = self.sshkey_set.filter(validated=True, selected=True)
        return key[0].key if len(key) > 0 else None

    @property
    def key(self):
        return self.get_key()
