#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_chat.api module

This module provides REST API for chat services.
"""

import json
from datetime import datetime
import sys

from colander import MappingSchema, OneOf, SchemaNode, String, drop
from cornice import Service
from pyramid.httpexceptions import HTTPAccepted, HTTPBadRequest, HTTPForbidden, HTTPNotFound, \
    HTTPOk, HTTPServiceUnavailable, HTTPUnauthorized

from pyams_chat.interfaces import IChatMessageHandler, REST_CONTEXT_ROUTE, \
    REST_NOTIFICATIONS_ROUTE
from pyams_chat.message import ChatMessage


__docformat__ = 'restructuredtext'

from pyams_chat import _


TEST_MODE = sys.argv[-1].endswith('/test')


class StatusSchema(MappingSchema):
    """Base status response schema"""
    status = SchemaNode(String(),
                        title=_("Response status"),
                        validator=OneOf(('success', 'error')))


class ContextSchema(StatusSchema):
    """User context schema"""
    principal = SchemaNode(String(),
                           title=_("Principal ID"))


class ErrorSchema(MappingSchema):
    """Base error schema"""
    status = SchemaNode(String(),
                        title=_("Response status"))
    message = SchemaNode(String(),
                         title=_("Error message"),
                         missing=drop)


jwt_responses = {
    HTTPOk.code: ContextSchema(description=_("User context properties")),
    HTTPAccepted.code: StatusSchema(description=_("Token accepted")),
    HTTPNotFound.code: ErrorSchema(description=_("Page not found")),
    HTTPUnauthorized.code: ErrorSchema(description=_("Unauthorized")),
    HTTPForbidden.code: ErrorSchema(description=_("Forbidden access")),
    HTTPBadRequest.code: ErrorSchema(description=_("Missing arguments")),
    HTTPServiceUnavailable.code: ErrorSchema(description=_("Service unavailable"))
}

if TEST_MODE:
    service_params = {}
else:
    service_params = {
        'response_schemas': jwt_responses
    }


chat_service = Service(name=REST_CONTEXT_ROUTE,
                       pyramid_route=REST_CONTEXT_ROUTE,
                       description="PyAMS chat context API")


@chat_service.get(require_csrf=False,
                  **service_params)
def get_chat_context(request):
    """REST chat context service"""
    principal = request.principal
    message = ChatMessage.create_empty_message(request)
    adapters = [
        name
        for name, adapter in request.registry.getAdapters((message, ),
                                                          IChatMessageHandler)
    ]
    return {
        'status': 'success',
        'principal': {
            'id': principal.id,
            'title': principal.title,
            'principals': tuple(request.effective_principals)
        },
        'context': {
            '*': adapters
        }
    }


notifications_service = Service(name=REST_NOTIFICATIONS_ROUTE,
                                pyramid_route=REST_NOTIFICATIONS_ROUTE,
                                description='PyAMS chat notifications API')


@notifications_service.get(require_csrf=False,
                           **service_params)
def get_notifications(request):
    """REST notifications service"""

    def filter_messages(messages):
        """Filter user notifications"""
        for message in messages:
            if isinstance(message, (str, bytes)):
                message = json.loads(message)
            # don't get messages from other hosts
            if message.get('host') != request.host_url:
                continue
            # don't get messages from current user
            if message.get('source', {}).get('id') == request.principal.id:
                continue
            # filter message targets
            target = message.get('target', {})
            if set(request.effective_principals) & set(target.get('principals', ())):
                yield message

    timestamp = datetime.utcnow().timestamp()
    client = request.redis_client
    if client is None:
        return {
            "timestamp": timestamp,
            "notifications": []
        }
    settings = request.registry.settings
    notifications_key = settings.get('pyams_chat.notifications_key', 'chat:notifications')
    notifications = client.redis.lrange(f'{notifications_key}::{request.host_url}', 0, -1)
    return {
        "timestamp": timestamp,
        "notifications": list(filter_messages(notifications or ()))
    }
