"""Utility functions."""

from typing import Any, Iterator, List, Optional, Tuple

from instancelib.instances import Instance
import numpy as np


def export_safe(obj):
    """Safely export to transform into .json or .yaml."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def recursive_to_dict(nested: Any, exclude: Optional[List[str]] = None) -> Iterator[Tuple[str, Any]]:
    """Recursively transform objects into a dictionary representation.

    Args:
        nested (Any): Current object.
        exclude (Optional[List[str]], optional): Keys to exclude. Defaults to None.

    Yields:
        Iterator[Tuple[str, Any]]: Current level of key-value pairs.
    """
    exclude = [] if exclude is None else exclude
    if hasattr(nested, '__class__'):
        yield '__class__', str(nested.__class__).split("'")[1]
    if hasattr(nested, '__dict__'):
        nested = nested.__dict__
    for key, value in nested.items():
        if not key.startswith('__') and key not in exclude:
            if hasattr(value, '__dict__'):
                yield key, dict(recursive_to_dict(value, exclude=exclude))
            else:
                yield key, export_safe(value)
