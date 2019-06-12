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

from django.urls import path

from django.conf.urls import url, include

from django.contrib.auth.models import User as UserDjango
from rest_framework import routers, serializers, viewsets

from .models import User, SSHKey

from . import views
from rest_framework_swagger.views import get_swagger_view


# Serializers define the API representation.
class UserDjangoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserDjango
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserDjangoViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDjangoSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('login', 'name', 'email', 'creation_date', 'revoked', 'key')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SSHKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SSHKey
        fields = ('key', 'sum_md5', 'sum_sha256', 'creation_date', 'validated', 'selected', "user")


class SSHKeyViewSet(viewsets.ModelViewSet):
    queryset = SSHKey.objects.all()
    serializer_class = SSHKeySerializer


router = routers.DefaultRouter()
router.register(r'users_django', UserDjangoViewSet)
router.register(r'users', UserViewSet)
router.register(r'sshkeys', SSHKeyViewSet)

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', views.index, name='index'),
    path('save/', views.save_perms_on_host, name='save'),
    path('perms/', views.test_perms, name='perms'),
    url(r'^apidocs/$', schema_view)
]
