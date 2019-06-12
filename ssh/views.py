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

from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.http import require_http_methods

import redis
import json

from .core import Resolver, CacheDAO, RedisBackend, HostnameQueryHandler, TagQueryHandler, DefaultQueryHandler, QueryHandler
from .models import User, Permission, Host, HostGroup, HostTag, UnixUser, UnixUserGroup, UserGroup
from .models import QueryManager


# Create your views here.
@require_http_methods(["GET"])
def index(request):
    users = User.objects.all()

    uc = Resolver(cache_backend=CacheDAO())
    uc.generate_key()
    context = {
        "users": {
            user.login: user.get_key()
            for user in users
        },
        "perms": json.dumps(uc.perms, indent=4),
        "usergoups": {
            usergroup.name: ','.join(usergroup.unfold_members())
            for usergroup in UserGroup.objects.all()
        },
        "user_access": {
            user.login: user.host_access()
            for user in User.objects.all()
        }
    }
    print(context)
    return render(request, "ssh/index.html", context)


@require_http_methods(["GET"])
def save_perms_on_host(request):
    redis1 = redis.Redis(db=1)
    redis2 = redis.Redis(db=2)
    uc = Resolver(cache_backend=RedisBackend(redis1=redis1, redis2=redis2))
    uc.generate_key()
    uc.save()
    context = {
        "perms": uc.cache_backend.get_perms()
    }

    return render(request, "ssh/save.html", context)


@require_http_methods(["GET"])
def test_perms(request):
    redis1 = redis.Redis(db=1)
    redis2 = redis.Redis(db=2)
    uc = Resolver(cache_backend=RedisBackend(redis1=redis1, redis2=redis2))

    result = request.GET.dict()
    for manager in QueryManager.objects.order_by('order'):

        query_manager = QueryHandler(options=manager.parameters)
        if manager.query_handler == "HostnameQueryHandler":
            query_manager = HostnameQueryHandler(options=manager.parameters)
            result["response_from"] = manager.query_handler
        elif manager.query_handler == "TagQueryHandler":
            query_manager = TagQueryHandler(options=manager.parameters)
            result["response_from"] = manager.query_handler
        if manager.query_handler == "DefaultQueryHandler":
            query_manager = DefaultQueryHandler(options=manager.parameters)
            result["response_from"] = manager.query_handler

        response = query_manager.perms(request, uc.cache_backend)

        if response is not None:
            return HttpResponse('{"parameters": ' + json.dumps(result) + ', "perms":' + response.decode() + '}')

    return HttpResponse(status=500)
