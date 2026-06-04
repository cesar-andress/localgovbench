"""Inter-rater reliability metrics (Cohen's Kappa, Krippendorff's Alpha)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True, slots=True)
class ReliabilityResult:
    """Reliability statistics for one variable or study aggregate."""

    metric: str
    value: float
    n_units: int
    n_raters: int
    interpretation: str


def _validate_paired(rater_a: Sequence[int], rater_b: Sequence[int]) -> None:
    if len(rater_a) != len(rater_b):
        raise ValueError("Rater vectors must have equal length.")
    if not rater_a:
        raise ValueError("Empty rating vectors.")


def cohens_kappa(rater_a: Sequence[int], rater_b: Sequence[int]) -> float:
    """
    Cohen's Kappa for nominal/ordinal agreement between two raters.

    Values in [−1, 1]; 1 indicates perfect agreement.
    """
    _validate_paired(rater_a, rater_b)
    n = len(rater_a)
    categories = sorted(set(rater_a) | set(rater_b))
    observed = sum(1 for i in range(n) if rater_a[i] == rater_b[i]) / n

    dist_a = Counter(rater_a)
    dist_b = Counter(rater_b)
    expected = sum((dist_a[c] / n) * (dist_b[c] / n) for c in categories)

    if expected >= 1.0:
        return 1.0 if observed >= 1.0 else 0.0
    return (observed - expected) / (1.0 - expected)


def krippendorff_alpha(
    ratings: Sequence[Sequence[int | None]],
    *,
    max_value: int = 4,
) -> float:
    """
    Krippendorff's Alpha (ordinal) for >=2 coders and >=1 unit.

    *ratings* is a list of coder vectors (same length = number of units).
    ``None`` denotes missing values.
    """
    if len(ratings) < 2:
        raise ValueError("Krippendorff's Alpha requires at least two raters.")
    n_units = len(ratings[0])
    if n_units == 0:
        raise ValueError("No rating units provided.")
    for row in ratings:
        if len(row) != n_units:
            raise ValueError("All rater vectors must have equal length.")

    values = list(range(max_value + 1))
    v_max = max_value

    def ordinal_delta(v1: int, v2: int) -> float:
        return ((v1 - v2) / v_max) ** 2 if v_max else 0.0

    d_obs = 0.0
    d_exp = 0.0
    n_pairs = 0

    for unit_idx in range(n_units):
        unit_vals = [row[unit_idx] for row in ratings if row[unit_idx] is not None]
        if len(unit_vals) < 2:
            continue
        for i, v1 in enumerate(unit_vals):
            for v2 in unit_vals[i + 1 :]:
                d_obs += ordinal_delta(v1, v2)
                n_pairs += 1
        counts = Counter(unit_vals)
        m = len(unit_vals)
        for v1 in values:
            for v2 in values:
                prob = (counts[v1] / m) * (counts[v2] / m)
                d_exp += prob * ordinal_delta(v1, v2)

    if n_pairs == 0:
        return 1.0
    d_obs /= n_pairs
    if d_exp == 0:
        return 1.0
    return 1.0 - (d_obs / d_exp)


def interpret_kappa(kappa: float) -> str:
    """Landis & Koch (1977) reference labels (research guidance only)."""
    if kappa < 0:
        return "Poor (less than chance agreement)"
    if kappa < 0.20:
        return "Slight agreement"
    if kappa < 0.40:
        return "Fair agreement"
    if kappa < 0.60:
        return "Moderate agreement"
    if kappa < 0.80:
        return "Substantial agreement"
    return "Almost perfect agreement"


def interpret_alpha(alpha: float) -> str:
    """Common research thresholds for Krippendorff's Alpha."""
    if alpha < 0.667:
        return "Tentative (exploratory only)"
    if alpha < 0.800:
        return "Acceptable for tentative conclusions"
    return "Strong agreement"
