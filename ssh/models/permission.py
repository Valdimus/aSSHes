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

"""Define the permission model"""

from django.db import models

from .host_models.host_base import HostBase
from .unix_user.unix_user import UnixUser
from .user_models.user_base import UserBase
from .user_models.user import User

from .host_models.host import Host
from .host_models.host_group import HostGroup
from .host_models.host_tag import HostTag

from .unix_user.unix_user_group import UnixUserGroup


class Permission(models.Model):
    """Permission"""
    host_target = models.ForeignKey(HostBase, on_delete=models.CASCADE, blank=True, null=True)
    unix_target = models.ManyToManyField(UnixUser, related_name="unix_target")
    user_target = models.ManyToManyField(UserBase, related_name="user_target")

    def unfold_hosts(self):
        """Unfold hosts"""
        hosts = []

        if isinstance(self.host_target, Host):
            hosts = [self.host_target.fqdn]
        elif isinstance(self.host_target, HostGroup):
            hosts = self.host_target.unfold_members()
        elif isinstance(self.host_target, HostTag):
            hosts = [self.host_target.name]

        return hosts

    def unfold_users(self):
        """Unfold permissions"""
        return []

    def unfold_unix_users(self):
        unix_users = []
        for unix_target in self.unix_target.all():

            if isinstance(unix_target, UnixUserGroup):
                unix_users = unix_target.unfold_members()
            elif isinstance(unix_target, UnixUser):
                unix_users = [unix_target.name]
        return unix_users

    def user_access(self):
        return "unix_user=%s => host=%s" % (','.join(self.unfold_unix_users()), ','.join(self.unfold_hosts()))

    def __str__(self):
        return "%s -- %s -- %s" % (self.host_target, ','.join([str(i) for i in self.unix_target.all()]), ",".join([str(i) for i in self.user_target.all()]))