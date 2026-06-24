"""
TalentDNA AI - explainability Module
"""

class ExplainabilityEngine:

    def __init__(self):
        pass

    def explain(
        self,
        candidate,
        career_score,
        signal_score
    ):

        reasons = []

        if candidate.get(
            "years_experience",
            0
        ) >= 5:

            reasons.append(
                f"{candidate['years_experience']} years experience"
            )

        if candidate.get(
            "num_skills",
            0
        ) >= 10:

            reasons.append(
                "strong skill portfolio"
            )

        if career_score >= 20:

            reasons.append(
                "strong production engineering background"
            )

        if signal_score >= 40:

            reasons.append(
                "high recruiter engagement signals"
            )

        return ". ".join(reasons)