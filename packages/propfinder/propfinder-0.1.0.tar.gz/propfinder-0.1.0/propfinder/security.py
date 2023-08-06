#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import (
    Authenticated,
    Everyone,
)

from .models import User


class PropFinderAuthenticationPolicy(AuthTktAuthenticationPolicy):

    def authenticated_userid(self, request):
        user = request.user
        if user is not None:
            return user.id

    def effective_principals(self, request):
        principals = [Everyone]
        user = request.user
        if user is not None:
            principals.append(Authenticated)
            principals.append('user:%s' % (str(user.id),))
            principals.append('role:%s' % (user.role,))
        return principals


def get_user(request):
    user_id = request.unauthenticated_userid
    if user_id is not None:
        user = request.dbsession.query(User).get(user_id)
        return user


def includeme(config):
    settings = config.get_settings()
    authn_policy = PropFinderAuthenticationPolicy(
        settings.get('auth.secret', ''),
        hashalg='sha512',
        reissue_time=settings.get('session.reissue_time', None),
        max_age=settings.get('session.max_age', None)
    )
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.add_request_method(get_user, 'user', reify=True)
    config.set_default_permission("guest")

