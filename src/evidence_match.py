"""
TalentDNA AI - Evidence Match Engine

Searches candidate experience_text for evidence of
relevant technical work. Uses word-boundary-aware matching
and tiered keyword importance.

Key fix from audit:
- Word boundary matching to prevent 'ml' matching 'html'
- Context-aware: 'search' in 'search engine' vs 'job search'
- Tiered scoring: core_ai > ai_ml > data > software
"""

import re
from src.config import (
    CORE_AI_KEYWORDS,
    AI_ML_KEYWORDS,
    DATA_ENGINEERING_KEYWORDS,
    SOFTWARE_KEYWORDS
)


class EvidenceMatchEngine:

    def __init__(self):
        self.core_ai_keywords = CORE_AI_KEYWORDS
        self.ai_keywords = AI_ML_KEYWORDS
        self.data_keywords = DATA_ENGINEERING_KEYWORDS
        self.software_keywords = SOFTWARE_KEYWORDS

        # Pre-compile regex patterns for word boundary matching
        self._core_patterns = self._compile_patterns(
            self.core_ai_keywords
        )
        self._ai_patterns = self._compile_patterns(
            self.ai_keywords
        )
        self._data_patterns = self._compile_patterns(
            self.data_keywords
        )
        self._software_patterns = self._compile_patterns(
            self.software_keywords
        )

    def _compile_patterns(self, keywords):
        """Compile word-boundary regex patterns for keywords."""
        patterns = []
        for kw in keywords:
            # Use word boundaries to avoid partial matches
            # e.g., 'ml' won't match 'html'
            pattern = re.compile(
                r'\b' + re.escape(kw) + r'\b',
                re.IGNORECASE
            )
            patterns.append((kw, pattern))
        return patterns

    def _count_matches(self, text, patterns):
        """Count keyword matches with word boundaries."""
        count = 0
        matched = []
        for kw, pattern in patterns:
            if pattern.search(text):
                count += 1
                matched.append(kw)
        return count, matched

    def score(self, candidate):
        """Score candidate based on evidence in experience text."""

        # Search in experience_text (from career descriptions)
        experience_text = candidate.get(
            "experience_text", ""
        ).lower()

        # Also check summary for evidence
        summary = candidate.get(
            "summary", ""
        ).lower()

        # Also check headline
        headline = candidate.get(
            "headline", ""
        ).lower()

        # Combine all text sources
        full_text = " ".join([
            experience_text,
            summary,
            headline
        ])

        score = 0

        # ==========================
        # Core AI Search / Ranking (highest value)
        # ==========================

        core_count, core_matched = self._count_matches(
            full_text, self._core_patterns
        )
        score += core_count * 5

        # ==========================
        # AI / ML
        # ==========================

        ai_count, ai_matched = self._count_matches(
            full_text, self._ai_patterns
        )
        score += ai_count * 3

        # ==========================
        # Data Engineering
        # ==========================

        data_count, data_matched = self._count_matches(
            full_text, self._data_patterns
        )
        score += data_count * 2

        # ==========================
        # Software Engineering
        # ==========================

        sw_count, sw_matched = self._count_matches(
            full_text, self._software_patterns
        )
        score += sw_count * 1

        return score

    def get_evidence_details(self, candidate):
        """Return detailed evidence breakdown for explainability."""

        experience_text = candidate.get(
            "experience_text", ""
        ).lower()
        summary = candidate.get("summary", "").lower()
        headline = candidate.get("headline", "").lower()
        full_text = " ".join([experience_text, summary, headline])

        _, core_matched = self._count_matches(
            full_text, self._core_patterns
        )
        _, ai_matched = self._count_matches(
            full_text, self._ai_patterns
        )
        _, data_matched = self._count_matches(
            full_text, self._data_patterns
        )
        _, sw_matched = self._count_matches(
            full_text, self._software_patterns
        )

        return {
            "core_ai": core_matched,
            "ai_ml": ai_matched,
            "data_eng": data_matched,
            "software": sw_matched
        }