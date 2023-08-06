# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Component for creating external identifiers."""

from invenio_records_resources.services.records.components import ServiceComponent


class ExternalIdentifierComponent(ServiceComponent):
    """External identifier registration component."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Create identifier when record is created."""
        type(record).number.assign(record)
