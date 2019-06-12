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

"""Define model for SSHKey"""

from django.db import models

from .user_models.user import User


class SSHKey(models.Model):
    """SSHkey of User"""
    key = models.CharField(max_length=256, unique=True)
    sum_md5 = models.CharField(max_length=256, unique=True)
    sum_sha256 = models.CharField(max_length=256, unique=True)
    creation_date = models.DateTimeField('Creation date')
    validated = models.BooleanField(default=False)
    selected = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s(%s)" % (self.user.login, self.key)
