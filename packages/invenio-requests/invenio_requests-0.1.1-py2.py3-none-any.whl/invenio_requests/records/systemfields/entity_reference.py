# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Systemfield for managing referenced entities in request."""

from invenio_records.systemfields import SystemField

from ...resolvers.base import EntityProxy
from ...resolvers.registry import ResolverRegistry


class ReferencedEntityField(SystemField):
    """Systemfield for managing the request type."""

    def set_obj(self, instance, obj):
        """Set the referenced entity."""
        # allow the setter to be used with a reference dict,
        # an entity proxy, or an actual entity
        if not isinstance(obj, dict):
            if isinstance(obj, EntityProxy):
                obj = obj.reference_dict
            else:
                obj = ResolverRegistry.reference_entity(obj, raise_=True)

        # set dictionary key and reset the cache
        self.set_dictkey(instance, obj)
        self._set_cache(instance, None)

    def __set__(self, record, value):
        """Set the referenced entity."""
        assert record is not None
        self.set_obj(record, value)

    def obj(self, instance):
        """Get the referenced entity as an `EntityProxy`."""
        obj = self._get_cache(instance)
        if obj is not None:
            return obj

        reference_dict = self.get_dictkey(instance)
        obj = ResolverRegistry.resolve_entity_proxy(reference_dict)
        self._set_cache(instance, obj)
        return obj

    def __get__(self, record, owner=None):
        """Get the referenced entity as an `EntityProxy`."""
        if record is None:
            # access by class
            return self

        return self.obj(record)
