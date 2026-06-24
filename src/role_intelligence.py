"""
TalentDNA AI - Role Intelligence Engine

Scores candidates based on role title alignment with
the target JD. Uses tiered role lists from config.

Key design decisions:
- High-value roles get capped bonus (not additive per match)
- Low-value roles get hard penalty
- Unknown roles get neutral score (not penalized)
"""

from src.config import (
    HIGH_VALUE_ROLES,
    MEDIUM_VALUE_ROLES,
    LOW_VALUE_ROLES
)
import re


class RoleIntelligenceEngine:

    def __init__(self):
        self.high_value_roles = HIGH_VALUE_ROLES
        self.medium_value_roles = MEDIUM_VALUE_ROLES
        self.low_value_roles = LOW_VALUE_ROLES

        self._high_patterns = self._compile_patterns(self.high_value_roles)
        self._medium_patterns = self._compile_patterns(self.medium_value_roles)
        self._low_patterns = self._compile_patterns(self.low_value_roles)

    def _compile_patterns(self, roles):
        """Compile word-boundary regex patterns for roles."""
        return [re.compile(r'\b' + re.escape(role) + r'\b', re.IGNORECASE) for role in roles]

    def _check_roles(self, text, patterns):
        """Check if any role pattern appears in text."""
        for pattern in patterns:
            if pattern.search(text):
                return True
        return False

    def _count_roles(self, text, patterns):
        """Count how many role patterns appear in text."""
        count = 0
        for pattern in patterns:
            if pattern.search(text):
                count += 1
        return count

    def score(self, candidate):

        # Build role text from current title + all historical titles
        text = " ".join([
            candidate.get("current_title", ""),
            " ".join(
                candidate.get("job_titles", [])
            )
        ]).lower()

        current_title = candidate.get(
            "current_title", ""
        ).lower()

        score = 0

        # ==============================
        # Current title is most important
        # ==============================

        # Check current title specifically
        current_is_low = self._check_roles(
            current_title, self._low_patterns
        )
        current_is_high = self._check_roles(
            current_title, self._high_patterns
        )
        current_is_medium = self._check_roles(
            current_title, self._medium_patterns
        )

        if current_is_low:
            # Hard penalty for irrelevant current role (Disqualifier)
            score -= 1000
        elif current_is_high:
            score += 100
        elif current_is_medium:
            score += 40

        # ==============================
        # Historical titles add signal
        # (but capped — not infinitely additive)
        # ==============================

        historical_titles = candidate.get(
            "job_titles", []
        )

        high_history = 0
        low_history = 0

        for title in historical_titles:
            t = title.lower()
            if self._check_roles(t, self._high_patterns):
                high_history += 1
            elif self._check_roles(t, self._low_patterns):
                low_history += 1

        # Cap historical bonus at 60 (max 3 roles × 20)
        score += min(high_history, 3) * 20

        # Penalty if majority of career is low-value
        if len(historical_titles) > 0:
            low_ratio = low_history / len(historical_titles)
            if low_ratio > 0.5:
                score -= 50

        return score