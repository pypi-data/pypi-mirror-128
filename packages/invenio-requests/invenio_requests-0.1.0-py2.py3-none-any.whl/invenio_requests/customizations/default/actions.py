# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 TU Wien.
# Copyright (C) 2021 Northwestern University.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RequestActions define code to be executed when performing actions on requests."""


from invenio_access.permissions import system_process

from ...proxies import current_requests
from ...records.api import RequestEventFormat, RequestEventType
from ..base import RequestAction


class SubmitAction(RequestAction):
    """Submit a request."""

    def can_execute(self, identity, data=None):
        """Check whether the action can be executed."""
        return self.request.status == "draft"

    def execute(self, identity, data=None):
        """Execute the request action."""
        self.request.status = "open"

        request_id = self.request.number

        # Persist request changes
        self._commit()

        events_service = current_requests.request_events_service
        events_service.create(
            identity,
            request_id,
            {
                **data,
                "type": RequestEventType.COMMENT.value,
            },
        )


class AcceptAction(RequestAction):
    """Decline a request."""

    def can_execute(self, identity, data=None):
        """Check whether the action can be executed."""
        return self.request.status == "open"

    def execute(self, identity, data=None):
        """Execute the request action."""
        self.request.status = "accepted"

        request_id = self.request.number

        # Persist request changes
        self._commit()

        events_service = current_requests.request_events_service
        events_service.create(
            identity,
            request_id,
            {
                **data,
                "type": RequestEventType.ACCEPTED.value,
                "content": "",
                "format": RequestEventFormat.HTML.value,
            },
        )
        events_service.create(
            identity,
            request_id,
            {
                **data,
                "type": RequestEventType.COMMENT.value,
            },
        )


class DeclineAction(RequestAction):
    """Decline a request."""

    def can_execute(self, identity, data=None):
        """Check whether the action can be executed."""
        return self.request.status == "open"

    def execute(self, identity, data=None):
        """Execute the request action."""
        self.request.status = "declined"

        request_id = self.request.number

        # Persist request changes
        self._commit()

        events_service = current_requests.request_events_service
        events_service.create(
            identity,
            request_id,
            {
                "type": RequestEventType.DECLINED.value,
            }
        )
        events_service.create(
            identity,
            request_id,
            {
                **data,
                "type": RequestEventType.COMMENT.value,
            }
        )


class CancelAction(RequestAction):
    """Cancel a request."""

    def can_execute(self, identity, data=None):
        """Check whether the action can be executed."""
        return self.request.status == "open"

    def execute(self, identity, data=None):
        """Execute the request action."""
        self.request.status = "cancelled"

        request_id = self.request.number

        # Persist request changes
        self._commit()

        events_service = current_requests.request_events_service
        events_service.create(
            identity,
            request_id,
            {
                "type": RequestEventType.CANCELLED.value,
            }
        )
        events_service.create(
            identity,
            request_id,
            {
                **data,
                "type": RequestEventType.COMMENT.value,
            }
        )


class ExpireAction(RequestAction):
    """Expire a request."""

    def can_execute(self, identity, data=None):
        """Check whether the action can be executed."""
        is_system_process = system_process in identity.provides
        return self.request.is_open and is_system_process

    def execute(self, identity, data=None):
        """Execute the request action."""
        self.request.status = "expired"
