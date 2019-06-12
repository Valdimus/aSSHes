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

from django.contrib import admin

# Register your models here.
from .models import User, UserGroup, SSHKey, Host
from .models import HostGroup, TagType, Tag, HostTag
from .models import UnixUser, UnixUserGroup, Permission
from .models import QueryManager

class SSHKeyInLine(admin.TabularInline):
    model = SSHKey


class UserAdmin(admin.ModelAdmin):

    inlines = [SSHKeyInLine]


class UserInLine(admin.TabularInline):
    model = User


class UserGroupInLine(admin.TabularInline):
    model = UserGroup


class UserGroupAdmin(admin.ModelAdmin):
    inlines = [UserInLine, UserGroupInLine]


admin.site.register(User, UserAdmin)
admin.site.register(SSHKey)
admin.site.register(UserGroup)
admin.site.register(Host)
admin.site.register(HostGroup)
admin.site.register(TagType)
admin.site.register(Tag)
admin.site.register(HostTag)
admin.site.register(UnixUser)
admin.site.register(UnixUserGroup)
admin.site.register(Permission)
admin.site.register(QueryManager)
