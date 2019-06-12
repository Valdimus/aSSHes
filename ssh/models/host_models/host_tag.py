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


"""Define a host tag"""

from django.db import models

from ..tag_models.tag import Tag
from .host_base import HostBase


class HostTag(HostBase):
    """If host not have a group or not defined serve perms from Tag"""
    name = models.CharField(max_length=200, unique=True)
    tags = models.ManyToManyField(Tag, related_name="host_tags")

    def get_perms(self):
        """Get perm for this combinaison of tag"""
        pass

    def __str__(self):
        return self.name

    def compute_name(self):
        return "-".join([
            "%s:%s" % (i[0], i[1])
            for i in sorted([
                (tag.tag_type.name, tag.value)
                for tag in self.tags.all()
            ])
        ])
