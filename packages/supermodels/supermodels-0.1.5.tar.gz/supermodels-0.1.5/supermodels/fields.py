"""Includes special field types in the supermodels package."""
from dataclasses import field

from supermodels.util import get_timestamp, get_uuid


masked_field = lambda: field(metadata=dict(mask=True), kw_only=True)
uuid_field = lambda: field(default_factory=get_uuid, kw_only=True)
timestamp_field = lambda: field(default_factory=get_timestamp, repr=False, kw_only=True)
version_field = lambda: field(default_factory=lambda: 1, repr=False, kw_only=True)
