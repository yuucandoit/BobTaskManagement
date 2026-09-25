from typing import Tuple

def calculate_estimation_from_diff(diff_loc: int, task_type: str = "feature") -> Tuple[float, int]:
    """
    Returns (estimated_hours, story_points) derived from changed lines of code and task type.
    """
    multiplier = 1.0
    if task_type in ["bugfix", "chore"]:
        multiplier = 0.8
    elif task_type in ["docs"]:
        multiplier = 0.4
    elif task_type in ["refactor"]:
        multiplier = 1.2

    # Baseline: ~35 lines of code per estimated engineering hour
    raw_hours = max(0.5, (diff_loc / 35.0) * multiplier)
    estimated_hours = round(raw_hours, 1)

    # Fibonacci story points based on diff_loc
    if diff_loc < 60:
        story_points = 1
    elif diff_loc < 180:
        story_points = 2
    elif diff_loc < 350:
        story_points = 3
    elif diff_loc < 700:
        story_points = 5
    else:
        story_points = 8

    return estimated_hours, story_points


def check_scope_creep(actual_diff_loc: int, baseline_estimation_hours: float) -> Tuple[bool, float]:
    """
    Checks if actual diff size is more than 3x the baseline expectation.
    Baseline expectation is ~40 LOC per estimated hour.
    """
    if baseline_estimation_hours <= 0:
        baseline_estimation_hours = 1.0

    expected_loc = baseline_estimation_hours * 40.0
    ratio = round(actual_diff_loc / expected_loc, 2)

    is_scope_creep = ratio >= 3.0
    return is_scope_creep, ratio
