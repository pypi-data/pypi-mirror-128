# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Systemfields for request records."""

from .entity_reference import ReferencedEntityField
from .identity import IdentityField
from .open_state import OpenStateCalculatedField
from .request_type import RequestTypeField
from .status import RequestStatusField

__all__ = (
    "IdentityField",
    "OpenStateCalculatedField",
    "ReferencedEntityField",
    "RequestStatusField",
    "RequestTypeField",
)
