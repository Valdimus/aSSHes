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

"""Define host group"""


from django.db import models

from .host_base import HostBase
from .host import Host
from .host_tag import HostTag


class HostGroup(HostBase):
    """Group of host"""
    name = models.CharField(max_length=200, unique=True)
    members = models.ManyToManyField(HostBase, related_name="members")

    def unfold_members(self, already_unfold=None):
        """
        Get all user of the group
        :param already_unfold:
        :return:
        """

        already_unfold = already_unfold if already_unfold is not None else []

        hosts = []
        for element in self.members.all():
            if isinstance(element, Host):
                if element.fqdn not in hosts:
                    hosts.append(element.compute_name())
            elif isinstance(element, HostTag):
                if element.name not in hosts:
                    hosts.append(element.compute_name())
            elif isinstance(element, HostGroup):
                if element.name in already_unfold:
                    continue
                already_unfold.append(element.name)
                for host in element.unfold_members(already_unfold):
                    if host not in hosts:
                        hosts.append(host)

        return hosts

    def compute_name(self):
        return self.name

    def __str__(self):
        return self.name