"""Content validity metrics (I-CVI, S-CVI/Ave, Lawshe CVR) for expert panel studies."""

from __future__ import annotations

from dataclasses import dataclass

# Common thresholds in content validity literature (research guidance only).
ICVI_THRESHOLD = 0.78
LAWSHE_CVR_MIN_RATIO = 0.99  # illustrative; use Lawshe table for formal NE


@dataclass(frozen=True, slots=True)
class ItemCVIResult:
    """Item-level Content Validity Index."""

    item_id: str
    i_cvi: float
    n_experts: int
    n_agree: int
    passes_threshold: bool


@dataclass(frozen=True, slots=True)
class ScaleCVIResult:
    """Scale-level content validity summary."""

    s_cvi_ave: float
    items: tuple[ItemCVIResult, ...]
    items_below_threshold: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LawsheCVRResult:
    """Lawshe Content Validity Ratio for one item."""

    item_id: str
    cvr: float
    n_essential: int
    n_experts: int
    passes_minimum: bool


def compute_item_cvi(
    item_id: str,
    expert_ratings: list[int],
    *,
    agree_minimum: int = 4,
    scale_max: int = 5,
) -> ItemCVIResult:
    """
    Item-level CVI (I-CVI): proportion of experts rating >= *agree_minimum*.

    Typical use: relevance or clarity on a 5-point Likert scale (1=low, 5=high).
    """
    if not expert_ratings:
        raise ValueError("expert_ratings must not be empty")
    for rating in expert_ratings:
        if rating < 1 or rating > scale_max:
            raise ValueError(f"Rating {rating} out of range 1–{scale_max}")
    n_agree = sum(1 for r in expert_ratings if r >= agree_minimum)
    i_cvi = n_agree / len(expert_ratings)
    return ItemCVIResult(
        item_id=item_id,
        i_cvi=round(i_cvi, 4),
        n_experts=len(expert_ratings),
        n_agree=n_agree,
        passes_threshold=i_cvi >= ICVI_THRESHOLD,
    )


def compute_scale_cvi_ave(
    item_ratings: dict[str, list[int]],
    *,
    agree_minimum: int = 4,
) -> ScaleCVIResult:
    """Compute I-CVI per item and S-CVI/Ave (mean of I-CVIs)."""
    if not item_ratings:
        raise ValueError("item_ratings must not be empty")
    items = tuple(
        compute_item_cvi(item_id, ratings, agree_minimum=agree_minimum)
        for item_id, ratings in sorted(item_ratings.items())
    )
    s_cvi_ave = sum(i.i_cvi for i in items) / len(items)
    below = tuple(i.item_id for i in items if not i.passes_threshold)
    return ScaleCVIResult(
        s_cvi_ave=round(s_cvi_ave, 4),
        items=items,
        items_below_threshold=below,
    )


def compute_lawshe_cvr(
    item_id: str,
    essential_flags: list[bool],
    *,
    minimum_cvr: float | None = None,
) -> LawsheCVRResult:
    """
    Lawshe CVR: proportion of experts rating the item as essential.

    *minimum_cvr* should come from Lawshe (1975) table for panel size if used formally.
    """
    if not essential_flags:
        raise ValueError("essential_flags must not be empty")
    n_essential = sum(essential_flags)
    cvr = n_essential / len(essential_flags)
    min_cvr = minimum_cvr if minimum_cvr is not None else LAWSHE_CVR_MIN_RATIO
    return LawsheCVRResult(
        item_id=item_id,
        cvr=round(cvr, 4),
        n_essential=n_essential,
        n_experts=len(essential_flags),
        passes_minimum=cvr >= min_cvr,
    )


def load_relevance_survey(path: str) -> dict[str, list[int]]:
    """Load expert relevance ratings from indicator_relevance_survey_results YAML."""
    from pathlib import Path

    from localgovbench.utils.io import load_yaml

    data = load_yaml(Path(path))
    panel = data.get("expert_ratings") or []
    aggregated: dict[str, list[int]] = {}
    for entry in panel:
        for item in entry.get("criterion_ratings") or []:
            cid = item["criterion_id"]
            aggregated.setdefault(cid, []).append(int(item["relevance_score"]))
    return aggregated
