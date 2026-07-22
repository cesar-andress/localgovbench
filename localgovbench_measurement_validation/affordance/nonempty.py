"""Non-empty classification for schema inventory and realization prep."""

from __future__ import annotations

import json
import re
from typing import Any

PLACEHOLDER_TOKENS = frozenset(
    {
        "nan",
        "none",
        "null",
        "n/a",
        "na",
        "-",
        "--",
        "n.v.t.",
        "n.v.t",
        "nvt",
        "niet beschikbaar",
    }
)

INVALID_URL_PLACEHOLDERS = frozenset(
    {
        "no",
        "not available",
        "not available.",
        "not publicly available",
        "not applicable",
        "not applicable - no custom code",
        "not applicable - proprietary vendor training data",
        "n/a",
        "na",
        "none",
        "null",
    }
)


def classify_value(value: Any) -> str:
    """Return a value class for auditability.

    Classes:
      null, empty_string, empty_list, empty_dict, placeholder_token,
      valid_negative_categorical, invalid_url_placeholder, nonempty
    """
    if value is None:
        return "null"
    if isinstance(value, list):
        return "empty_list" if len(value) == 0 else "nonempty"
    if isinstance(value, dict):
        return "empty_dict" if len(value) == 0 else "nonempty"
    if isinstance(value, bool):
        return "nonempty"
    if isinstance(value, (int, float)):
        return "nonempty"

    text = str(value).strip()
    if text == "":
        return "empty_string"

    lowered = text.lower()
    if lowered in PLACEHOLDER_TOKENS:
        return "placeholder_token"

    # Valid negative / boolean-like categorical responses count as populated.
    if lowered in {"n", "no", "false", "0", "not high-impact"}:
        return "valid_negative_categorical"
    if text in {"N", "No", "Y", "Yes", "[]"}:
        # bare [] string sometimes appears; treat empty-list-as-string separately
        if text == "[]":
            return "empty_list"
        return "nonempty" if text in {"Y", "Yes"} else "valid_negative_categorical"

    if lowered in INVALID_URL_PLACEHOLDERS or lowered.startswith("not available"):
        return "invalid_url_placeholder"

    return "nonempty"


def is_nonempty_for_population(value: Any) -> bool:
    """True if the field is populated for disclosure realization rates.

    Valid No/N and invalid URL placeholders still count as populated values
    (the latter fail linkage realization, not field population).
    """
    cls = classify_value(value)
    return cls in {
        "nonempty",
        "valid_negative_categorical",
        "invalid_url_placeholder",
    }


def infer_data_type(samples: list[Any]) -> str:
    """Infer a coarse datatype from nonempty samples."""
    nonempty_samples = [v for v in samples if is_nonempty_for_population(v)]
    if not nonempty_samples:
        return "unknown_empty"

    scores: dict[str, int] = {}

    def bump(label: str) -> None:
        scores[label] = scores.get(label, 0) + 1

    url_re = re.compile(r"^https?://", re.I)
    path_re = re.compile(r"^/[\w\-./]+$")
    bool_re = re.compile(r"^(Y|N|Yes|No|true|false)$", re.I)
    num_re = re.compile(r"^-?\d+(\.\d+)?$")
    date_re = re.compile(r"^\d{4}([-T/]\d{2})?")

    for value in nonempty_samples[:300]:
        if isinstance(value, list):
            bump("list")
            continue
        if isinstance(value, dict):
            bump("dict")
            continue
        if isinstance(value, bool):
            bump("boolean")
            continue
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            bump("number")
            continue
        text = str(value).strip()
        if url_re.match(text) or path_re.match(text):
            bump("url_or_path")
        elif bool_re.match(text):
            bump("booleanish")
        elif num_re.match(text):
            bump("numeric_str")
        elif date_re.match(text) or (text.endswith("Z") and "T" in text):
            bump("dateish")
        elif len(text) <= 60:
            bump("categorical_or_short_text")
        else:
            bump("text")

    priority = [
        "list",
        "dict",
        "url_or_path",
        "booleanish",
        "boolean",
        "dateish",
        "numeric_str",
        "number",
        "categorical_or_short_text",
        "text",
    ]
    for label in priority:
        if scores.get(label):
            if label == "categorical_or_short_text":
                # Prefer categorical when value cardinality is low.
                uniq = {
                    str(v).strip()
                    for v in nonempty_samples
                    if is_nonempty_for_population(v)
                }
                return "categorical" if len(uniq) <= 40 else "text"
            return label
    return "text"


def dump_jsonable(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(value)
