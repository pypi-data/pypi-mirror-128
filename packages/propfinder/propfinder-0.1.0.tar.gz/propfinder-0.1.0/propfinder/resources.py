#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
from pyramid.security import (
    Allow,
    DENY_ALL
)

from chisel.modeling import cached_getter
from chisel.resources import CRUDResource
from chisel.pkgutils import resolve

from propfinder.models import (
    User,
    Location,
    URL,
    Property
)


class RootResource(object):

    def __init__(self, request):
        self.request = request

    def __acl__(self):
        return [
            DENY_ALL
        ]


class PageResource(RootResource):

    def __acl__(self):
        return [
            (Allow, 'role:admin', 'view'),
            DENY_ALL
        ]


class AdminResource(RootResource):

    def __acl__(self):
        return [
            (Allow, 'role:admin', 'view'),
            DENY_ALL
        ]


class LocationResource(CRUDResource):

    model = Location
    route_base_name = 'locations'

    def __acl__(self):
        return [
            (Allow, 'role:admin', 'view'),
            (Allow, 'role:admin', 'edit'),
            DENY_ALL
        ]


class UserResource(CRUDResource):

    model = User
    route_base_name = 'users'

    def __acl__(self):
        return [
            (Allow, 'role:admin', 'view'),
            (Allow, 'role:admin', 'edit'),
            (Allow, 'role:admin', 'admin'),
            DENY_ALL
        ]


class URLResource(CRUDResource):

    model = URL
    route_base_name = 'urls'

    def __acl__(self):
        return [
            (Allow, 'role:admin', 'view'),
            (Allow, 'role:admin', 'create'),
            (Allow, 'role:admin', 'edit'),
            DENY_ALL
        ]


class PropertyResource(CRUDResource):

    model = Property
    route_base_name = 'properties'

    def __acl__(self):
        return [
            (Allow, 'role:admin', 'view'),
            (Allow, 'role:admin', 'edit'),
            DENY_ALL
        ]


class ProfileResource(object):

    def __init__(self, request):
        self.request = request
        self.item = self.request.user

    @property
    def item_id(self):
        return self.item.id

    @property
    def model(self):
        return self.item.__class__

    def __acl__(self):
        return [
            (Allow, 'user:%s' % (self.item.id,), 'edit'),
            DENY_ALL
        ]

