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

"""Define a host"""

from django.db import models

from .host_base import HostBase


class Host(HostBase):
    """The host"""
    fqdn = models.CharField(max_length=256, unique=True)
    ip = models.CharField(max_length=100)
    latest_seen = models.DateTimeField("Latest time host comes to get his keys")

    def get_perms(self):
        """Get perms for this host"""
        pass

    def compute_name(self):
        return self.fqdn

    def __str__(self):
        return self.fqdn