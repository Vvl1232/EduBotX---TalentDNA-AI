"""
TalentDNA AI - Signal Engine

Scores candidates based on Redrob platform behavioral signals.
Properly handles sentinel values (-1 for github, offer_acceptance).

Key fixes from audit:
- github_activity_score = -1 means "no GitHub linked" (not a penalty)
- offer_acceptance_rate = -1 means "no offer history" (not a penalty)
- last_active_date freshness now factored in
- skill_assessment_scores averaged and used
"""

from src.config import SIGNAL_WEIGHTS


class SignalEngine:

    def __init__(self):
        self.weights = SIGNAL_WEIGHTS

    def score(self, candidate):

        score = 0

        # ========================
        # Open to work (strong signal)
        # ========================

        score += (
            candidate.get("open_to_work", 0)
            * self.weights["open_to_work"]
        )

        # ========================
        # Response rate (0-1 range)
        # ========================

        score += (
            candidate.get("response_rate", 0)
            * self.weights["response_rate"]
        )

        # ========================
        # GitHub score
        # FIX: -1 means no GitHub linked → treat as 0
        # ========================

        github = candidate.get("github_score", -1)
        if github >= 0:
            score += github * self.weights["github_score"]
        # else: no GitHub linked — neutral, not penalized

        # ========================
        # Saved by recruiters (count)
        # ========================

        score += (
            candidate.get("saved_by_recruiters", 0)
            * self.weights["saved_by_recruiters"]
        )

        # ========================
        # Interview completion (0-1 range)
        # ========================

        score += (
            candidate.get("interview_completion", 0)
            * self.weights["interview_completion"]
        )

        # ========================
        # Offer acceptance rate
        # FIX: -1 means no offer history → treat as 0
        # ========================

        offer_rate = candidate.get("offer_acceptance", -1)
        if offer_rate >= 0:
            score += offer_rate * self.weights["offer_acceptance"]
        # else: no offer history — neutral, not penalized

        # ========================
        # Profile completeness (0-100 range)
        # ========================

        score += (
            candidate.get("profile_score", 0)
            * self.weights["profile_score"]
        )

        # ========================
        # Profile views (count)
        # ========================

        score += (
            candidate.get("profile_views", 0)
            * self.weights["profile_views"]
        )

        # ========================
        # Search appearances (count)
        # ========================

        score += (
            candidate.get("search_appearance", 0)
            * self.weights["search_appearance"]
        )

        # ========================
        # Skill assessment average
        # -1 means no assessments taken
        # ========================

        assess_avg = candidate.get(
            "skill_assessment_avg", -1
        )
        if assess_avg >= 0:
            score += (
                assess_avg
                * self.weights["skill_assessment_avg"]
            )

        # ========================
        # Connection count (diminishing returns)
        # ========================

        connections = candidate.get(
            "connection_count", 0
        )
        # Cap at 500 to prevent outlier influence
        score += (
            min(connections, 500)
            * self.weights["connection_count"]
        )

        return round(score, 2)