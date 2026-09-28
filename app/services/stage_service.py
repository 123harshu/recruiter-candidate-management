from typing import Tuple, List

VALID_STAGES: List[str] = [
    "Applied",
    "Screening",
    "Interview",
    "Offer",
    "Hired"
]

# Strict forward linear transitions allowed for recruiter workflow
ALLOWED_TRANSITIONS = {
    "Applied": ["Screening"],
    "Screening": ["Interview"],
    "Interview": ["Offer"],
    "Offer": ["Hired"],
    "Hired": []  # Terminal state
}


class StageTransitionError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def validate_stage_transition(current_stage: str, target_stage: str) -> Tuple[bool, str]:
    """
    Validates stage transition rules.
    Only sequential forward movement is permitted.
    """
    if target_stage not in VALID_STAGES:
        return False, f"Invalid stage '{target_stage}'. Valid stages are: {', '.join(VALID_STAGES)}"

    if current_stage not in VALID_STAGES:
        return False, f"Candidate is in invalid state '{current_stage}'"

    if current_stage == target_stage:
        return False, f"Candidate is already in '{target_stage}' stage."

    allowed = ALLOWED_TRANSITIONS.get(current_stage, [])
    if target_stage not in allowed:
        return False, f"Invalid stage transition: {current_stage} -> {target_stage}"

    return True, "Transition valid"