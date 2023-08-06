"""The supermodels package."""

from supermodels.models import (
    from_dict,
    from_json,
    is_supermodel,
    to_dict,
    to_json,
    supermodel,
)

from supermodels.rules import NewRules

__all__ = [
    "from_dict",
    "from_json",
    "is_supermodel",
    "NewRules",
    "to_dict",
    "to_json",
    "supermodel",
]
