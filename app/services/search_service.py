from datetime import datetime, timezone
from typing import List, Optional
from rapidfuzz import process, fuzz
from app.models import Candidate

FUZZY_RATIO_THRESHOLD = 60.0


def calculate_days_in_stage(updated_at: datetime) -> int:
    """Calculates integer days a candidate has been in their current stage."""
    if not updated_at:
        return 0
    
    # Ensure UTC timezone awareness
    if updated_at.tzinfo is None:
        updated_at = updated_at.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    delta = now - updated_at
    return max(0, delta.days)


def apply_search_and_filters(
    candidates: List[Candidate],
    search_query: Optional[str] = None,
    stage_filter: Optional[str] = None,
    min_days: Optional[int] = None,
    max_days: Optional[int] = None
) -> List[Candidate]:
    """
    Applies combined filters:
    1. RapidFuzz name search on candidate full_name.
    2. Stage exact match.
    3. Min and Max days in current stage.
    """
    filtered = candidates

    # 1. Exact Stage Filter
    if stage_filter and stage_filter.strip():
        s_clean = stage_filter.strip().title()
        filtered = [c for c in filtered if c.current_stage == s_clean]

    # 2. Time-in-stage Filter
    if min_days is not None or max_days is not None:
        result = []
        for c in filtered:
            days = calculate_days_in_stage(c.updated_at)
            if min_days is not None and days < min_days:
                continue
            if max_days is not None and days > max_days:
                continue
            result.append(c)
        filtered = result

    # 3. RapidFuzz Fuzzy Search
    if search_query and search_query.strip():
        q = search_query.strip()
        names = [c.full_name for c in filtered]

        if names:
            # Partial ratio allows matching substring/first names ("Harsh" -> "Harshita Verma")
            matches = process.extract(
                q,
                names,
                scorer=fuzz.partial_ratio,
                score_cutoff=FUZZY_RATIO_THRESHOLD,
                limit=len(names)
            )
            
            matched_indices = {idx for _, score, idx in matches}
            filtered = [c for idx, c in enumerate(filtered) if idx in matched_indices]

    return filtered