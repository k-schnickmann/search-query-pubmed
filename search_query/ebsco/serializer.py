#!/usr/bin/env python3
"""EBSCO serializer"""
from __future__ import annotations

import typing


if typing.TYPE_CHECKING:  # pragma: no cover
    from search_query.query import Query

# pylint: disable=too-few-public-methods


def to_string_ebsco(query: Query) -> str:
    """Convert the query to a string representation for EBSCO."""
    # pylint: disable=import-outside-toplevel
    from search_query.query_near import NEARQuery

    query = query.copy()

    if not query.children:
        # Leaf query (single search term)
        field = f"{query.search_field.value} " if query.search_field else ""
        return f"{field}{query.value}"

    result = []
    needs_parentheses = len(query.children) > 1  # Parentheses needed for grouping

    for i, child in enumerate(query.children):
        child_str = to_string_ebsco(child)

        if isinstance(query, NEARQuery):
            # Convert proximity operator to EBSCO format
            proximity_operator = (
                f"{'N' if query.value == 'NEAR' else 'W'}{query.distance}"
            )

            # Ensure correct order of proximity terms
            if i == 0:
                result.append(child_str)
            else:
                result.append(f"{proximity_operator} {child_str}")
        else:
            if i > 0:  # Add the operator between terms
                result.append(query.value)

            result.append(child_str)

    query_str = " ".join(result)

    if needs_parentheses:
        query_str = f"({query_str})"

    if query.search_field:
        # Add search field if present
        query_str = f"{query.search_field.value} {query_str}"
    return query_str
