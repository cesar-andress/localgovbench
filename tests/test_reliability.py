"""Tests for reliability metrics."""

from __future__ import annotations

import pytest

from localgovbench.validation.reliability import cohens_kappa, krippendorff_alpha


def test_cohens_kappa_perfect_agreement() -> None:
    a = [0, 1, 2, 3, 4, 2, 2, 2]
    assert cohens_kappa(a, a) == pytest.approx(1.0)


def test_cohens_kappa_total_disagreement() -> None:
    a = [0, 0, 0, 0]
    b = [4, 4, 4, 4]
    kappa = cohens_kappa(a, b)
    assert kappa < 0.2


def test_krippendorff_alpha_perfect() -> None:
    a = [1, 2, 3, 4]
    b = [1, 2, 3, 4]
    assert krippendorff_alpha([a, b]) == pytest.approx(1.0, abs=0.01)


def test_krippendorff_alpha_requires_two_raters() -> None:
    with pytest.raises(ValueError):
        krippendorff_alpha([[1, 2, 3]])


def test_krippendorff_alpha_partial_agreement() -> None:
    a = [2, 2, 2, 3, 3]
    b = [2, 3, 2, 3, 4]
    alpha = krippendorff_alpha([a, b])
    assert 0.0 < alpha < 1.0
