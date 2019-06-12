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

from django.db import models

from .user_base import UserBase
from .user import User


class UserGroup(UserBase):
    """User Group"""
    name = models.CharField(max_length=200, unique=True)
    members = models.ManyToManyField(UserBase, related_name="members")
    external = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def unfold_members(self, already_unfold=None):
        """
        Get all user of the group
        :param already_unfold:
        :return:
        """
        already_unfold = already_unfold if already_unfold is not None else []
        users = []
        for element in self.members.all():
            if isinstance(element, User):
                key = element.get_key()
                if key is None:
                    continue
                if key not in users:
                    users.append(key)
            if isinstance(element, UserGroup):
                if element.name in already_unfold:
                    continue
                for key in element.unfold_members(already_unfold):
                    if key not in users:
                        users.append(key)
        return users

    def host_acess(self):
        """Get all host access for this group"""
        pass