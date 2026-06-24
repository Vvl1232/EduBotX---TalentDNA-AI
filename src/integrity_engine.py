"""
TalentDNA AI - Integrity Engine

Purpose:
- Detect honeypot profiles
- Detect inactive/unavailable candidates
- Detect consulting-only careers
- Detect templated/generic summaries
- Detect pure research profiles with no production evidence

Scoring: starts at 100, penalties subtract.
Used as a multiplier in final ranking (score × integrity/100).
A score of 0 effectively removes the candidate.

Audit (2026-06-23): Removed 5 dead rules (0% or <0.01% activation
across 100K candidates):
  - junior_skill_inflation  (0 fires)
  - junior_cert_inflation   (0 fires)
  - job_hopper              (0 fires)
  - low_response_rate       (12 fires / 100K = 0.01%, inert threshold)
  - stale_AND_low_rr combo  (7 fires / 100K, inert)

Fixed: pure_research_trap
  - Old: checked experience_text for generic terms ("pipeline", "scale")
         which appear in boilerplate descriptions of any candidate.
         Result: 0 fires across 100K candidates (broken).
  - New: checks profile summary for specific production deployment terms.
         Penalty set to -50 (not -100) pending activation audit.
         Avoids accidentally eliminating AI Research / Recommendation
         Researcher profiles before the rule is validated.
"""

from src.config import (
    CONSULTING_FIRMS,
    INTEGRITY_THRESHOLDS
)


class IntegrityEngine:

    def __init__(self):
        self.consulting_firms = CONSULTING_FIRMS
        self.thresholds = INTEGRITY_THRESHOLDS

    def score(self, candidate):

        score = 100

        # ================================
        # Rule 1: Consulting-only career
        # JD explicitly disqualifies candidates
        # who have only worked at consulting firms.
        # Activation: 9.7% (9,745 / 100K)
        # ================================

        career_companies = self._get_career_companies(candidate)

        if len(career_companies) > 0:
            consulting_count = sum(
                1 for company in career_companies
                if any(
                    firm in company.lower()
                    for firm in self.consulting_firms
                )
            )
            if consulting_count == len(career_companies):
                score -= 100  # Hard disqualification

        # ================================
        # Rule 2: Templated summary detection
        # Identifies synthetic Redrob honeypot profiles
        # sharing identical boilerplate summaries.
        # Activation: 63.3% (63,304 / 100K)
        # ================================

        summary = candidate.get("summary", "").lower()
        template_hits = sum(
            1 for phrase in self.thresholds["templated_summary_phrases"]
            if phrase in summary
        )

        if template_hits >= 2:
            score -= 25
        elif template_hits >= 1:
            score -= 10

        # ================================
        # Rule 3: Activity freshness
        # JD says profiles inactive 6+ months
        # are not actually available.
        # Activation: 28.6% (28,615 / 100K)
        # ================================

        days_since_active = candidate.get("days_since_active", 0)
        if days_since_active > self.thresholds["freshness_stale_days"]:
            score -= 15

        # ================================
        # Rule 4: Pure research trap (FIXED)
        #
        # Old implementation was broken:
        #   - Checked experience_text which always contains
        #     generic terms like "pipeline" or "scale"
        #     from any boilerplate job description.
        #   - Result: 0 fires across 100K candidates.
        #
        # New implementation:
        #   - Checks current_title AND headline for research signal.
        #   - Checks profile summary (self-described) for specific
        #     production deployment evidence.
        #   - Penalty is -50 (not -100) for initial benchmark.
        #     Escalate to -100 only after confirming no legitimate
        #     AI Research / Recommendation Researcher profiles
        #     are eliminated from the Top 100.
        # ================================

        current_title = candidate.get("current_title", "").lower()
        headline = candidate.get("headline", "").lower()

        is_research_profile = (
            "research" in current_title
            or "academic" in current_title
            or "research" in headline
        )

        if is_research_profile:
            summary_lower = candidate.get("summary", "").lower()
            production_evidence = [
                "production",
                "deployed",
                "served",
                "real-time",
                "serving",
                "at scale",
                "billions",
                "millions of",
                "low latency",
                "inference endpoint",
                "api",
                "model serving",
                "mlops"
            ]
            if not any(
                term in summary_lower
                for term in production_evidence
            ):
                score -= 50  # Soft penalty pending activation audit

        return max(score, 0)

    def _get_career_companies(self, candidate):
        """
        Extract full list of company names from career history.

        Priority:
        1. career_companies  — full history list, populated by
                               CareerFeatureExtractor (after bug fix)
        2. current_company   — fallback, checks current job only
                               (insufficient for consulting detection)
        """
        companies = candidate.get("career_companies", [])
        if companies:
            return companies

        # Fallback: current_company only.
        # WARNING: This path misses prior career history.
        # Consult bug report in career_features.py.
        current = candidate.get("current_company", "")
        if current:
            return [current]

        return []

    def get_flags(self, candidate):
        """Return detailed integrity flags for explainability."""
        flags = []

        summary = candidate.get("summary", "").lower()
        for phrase in self.thresholds["templated_summary_phrases"]:
            if phrase in summary:
                flags.append("templated_summary")
                break

        days_since_active = candidate.get("days_since_active", 0)
        if days_since_active > self.thresholds["freshness_stale_days"]:
            flags.append("inactive_profile")

        career_companies = self._get_career_companies(candidate)
        if len(career_companies) > 0:
            consulting_count = sum(
                1 for c in career_companies
                if any(f in c.lower() for f in self.consulting_firms)
            )
            if consulting_count == len(career_companies):
                flags.append("consulting_only")

        current_title = candidate.get("current_title", "").lower()
        headline = candidate.get("headline", "").lower()

        is_research_profile = (
            "research" in current_title
            or "academic" in current_title
            or "research" in headline
        )

        if is_research_profile:
            summary_lower = candidate.get("summary", "").lower()
            production_evidence = [
                "production",
                "deployed",
                "served",
                "real-time",
                "serving",
                "at scale",
                "billions",
                "millions of",
                "low latency",
                "inference endpoint",
                "api",
                "model serving",
                "mlops"
            ]
            if not any(
                term in summary_lower
                for term in production_evidence
            ):
                flags.append("pure_research_no_production")

        return flags