"""Helpers for mapping user-provided visual materials to script segments."""

from __future__ import annotations

import re
from collections.abc import Iterable

from app.models.schema import MaterialInfo


_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?。！？])\s+")


def split_script_segments(script: str, max_segments: int = 20) -> list[str]:
    """Split a short-form script into user-selectable narrative segments."""
    normalized = str(script or "").strip()
    if not normalized or max_segments < 1:
        return []

    paragraphs = [
        " ".join(part.split())
        for part in re.split(r"\n\s*\n+", normalized)
        if part.strip()
    ]
    if len(paragraphs) > 1:
        return paragraphs[:max_segments]

    sentences = [
        sentence.strip()
        for sentence in _SENTENCE_BOUNDARY.split(paragraphs[0])
        if sentence.strip()
    ]
    return (sentences or paragraphs)[:max_segments]


def order_materials_by_segment(
    materials: Iterable[MaterialInfo] | None,
) -> list[MaterialInfo]:
    """
    Order assigned materials by script segment and keep upload order stable.

    Unassigned files remain available as fallbacks after assigned materials.
    """
    material_list = list(materials or [])
    indexed = list(enumerate(material_list))
    indexed.sort(
        key=lambda item: (
            item[1].segment_index is None,
            (item[1].segment_index if item[1].segment_index is not None else item[0]),
            item[0],
        )
    )
    return [material for _, material in indexed]


def has_segment_assignments(
    materials: Iterable[MaterialInfo] | None,
) -> bool:
    """Return whether at least one material has an explicit script position."""
    return any(material.segment_index is not None for material in materials or [])
