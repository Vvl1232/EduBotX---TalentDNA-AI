"""
TalentDNA AI - Candidate Parser

Parses raw candidate JSON into a flat feature dictionary
for downstream scoring engines.
"""

import pandas as pd
from datetime import datetime, date


class CandidateParser:

    def __init__(self):
        pass

    # -------------------------
    # Skill Utilities
    # -------------------------

    def extract_skill_names(self, skills):
        return [
            skill.get("name", "")
            for skill in skills
            if skill.get("name")
        ]

    def build_skill_text(self, skills):
        return " ".join(
            self.extract_skill_names(skills)
        )

    # -------------------------
    # Certification Utilities
    # -------------------------

    def extract_certification_names(self, certifications):
        return [
            cert.get("name", "")
            for cert in certifications
            if cert.get("name")
        ]

    # -------------------------
    # Skill Assessment Utilities
    # -------------------------

    def extract_skill_assessment_avg(self, signals):
        """Extract average skill assessment score from Redrob platform tests."""
        scores = signals.get("skill_assessment_scores", {})
        if not scores:
            return -1  # sentinel: no assessments taken
        values = list(scores.values())
        if len(values) == 0:
            return -1
        return round(sum(values) / len(values), 2)

    def extract_skill_assessment_count(self, signals):
        """Count how many skill assessments were taken."""
        scores = signals.get("skill_assessment_scores", {})
        return len(scores)

    # -------------------------
    # Freshness / Activity
    # -------------------------

    def compute_days_since_active(self, signals):
        """Days since last_active_date. Lower = more active."""
        last_active = signals.get("last_active_date", None)
        if not last_active:
            return 999

        try:
            last_dt = datetime.strptime(
                str(last_active), "%Y-%m-%d"
            ).date()
            delta = date.today() - last_dt
            return max(delta.days, 0)
        except (ValueError, TypeError):
            return 999

    # -------------------------
    # Education Utilities
    # -------------------------

    def extract_education_features(self, education):
        """Extract education tier and field relevance."""
        best_tier = "unknown"
        tier_rank = {"tier_1": 1, "tier_2": 2, "tier_3": 3, "tier_4": 4, "unknown": 5}
        relevant_fields = [
            "computer science", "machine learning",
            "artificial intelligence", "data science",
            "information technology", "statistics",
            "mathematics", "electrical engineering",
            "electronics"
        ]
        has_relevant_degree = False
        highest_degree = ""
        degree_rank = {"Ph.D": 1, "M.Tech": 2, "M.E.": 2, "M.Sc": 3, "M.S.": 3, "B.Tech": 4, "B.E.": 4, "B.Sc": 5}

        for edu in education:
            tier = edu.get("tier", "unknown")
            if tier_rank.get(tier, 5) < tier_rank.get(best_tier, 5):
                best_tier = tier

            field = edu.get("field_of_study", "").lower()
            if any(rf in field for rf in relevant_fields):
                has_relevant_degree = True

            deg = edu.get("degree", "")
            if degree_rank.get(deg, 6) < degree_rank.get(highest_degree, 6):
                highest_degree = deg

        return {
            "education_tier": best_tier,
            "has_relevant_degree": int(has_relevant_degree),
            "highest_degree": highest_degree
        }

    # -------------------------
    # Main Parser
    # -------------------------

    def parse(self, row):

        profile = row["profile"]
        signals = row["redrob_signals"]
        skills = row["skills"]
        certifications = row.get("certifications", [])
        education = row.get("education", [])

        skill_names = self.extract_skill_names(skills)
        skill_text = self.build_skill_text(skills)

        certification_names = (
            self.extract_certification_names(certifications)
        )

        edu_features = self.extract_education_features(education)

        # =====================
        # RICH candidate_text for embedding
        # Includes: title, headline, summary, skills, certs
        # This is the #1 fix from the audit
        # =====================

        summary = profile.get("summary", "")
        headline = profile.get("headline", "")
        current_title = profile.get("current_title", "")

        candidate_text = " ".join(filter(None, [
            current_title,
            headline,
            summary,
            skill_text,
            " ".join(certification_names)
        ]))

        return {

            # =====================
            # Identity
            # =====================

            "candidate_id":
                row["candidate_id"],

            # =====================
            # Profile Features
            # =====================

            "headline": headline,

            "summary": summary,

            "location":
                profile.get("location", ""),

            "country":
                profile.get("country", ""),

            "years_experience":
                profile.get("years_of_experience", 0),

            "current_title": current_title,

            "current_company":
                profile.get("current_company", ""),

            "company_size":
                profile.get("current_company_size", ""),

            "industry":
                profile.get("current_industry", ""),

            # =====================
            # Skills
            # =====================

            "skill_names": skill_names,

            "skill_text": skill_text,

            "num_skills": len(skill_names),

            # =====================
            # Certifications
            # =====================

            "certification_names": certification_names,

            "num_certifications": len(certification_names),

            # =====================
            # Education
            # =====================

            **edu_features,

            # =====================
            # Recruiter Signals
            # =====================

            "profile_score":
                signals.get(
                    "profile_completeness_score", 0
                ),

            "open_to_work":
                int(signals.get(
                    "open_to_work_flag", False
                )),

            "response_rate":
                signals.get(
                    "recruiter_response_rate", 0
                ),

            "avg_response_time":
                signals.get(
                    "avg_response_time_hours", 0
                ),

            "profile_views":
                signals.get(
                    "profile_views_received_30d", 0
                ),

            "applications":
                signals.get(
                    "applications_submitted_30d", 0
                ),

            "github_score":
                signals.get(
                    "github_activity_score", -1
                ),

            "search_appearance":
                signals.get(
                    "search_appearance_30d", 0
                ),

            "saved_by_recruiters":
                signals.get(
                    "saved_by_recruiters_30d", 0
                ),

            "interview_completion":
                signals.get(
                    "interview_completion_rate", 0
                ),

            "offer_acceptance":
                signals.get(
                    "offer_acceptance_rate", -1
                ),

            "connection_count":
                signals.get(
                    "connection_count", 0
                ),

            "endorsements":
                signals.get(
                    "endorsements_received", 0
                ),

            "notice_period_days":
                signals.get(
                    "notice_period_days", 0
                ),

            "preferred_work_mode":
                signals.get(
                    "preferred_work_mode", ""
                ),

            "willing_to_relocate":
                int(signals.get(
                    "willing_to_relocate", False
                )),

            "verified_email":
                int(signals.get(
                    "verified_email", False
                )),

            "verified_phone":
                int(signals.get(
                    "verified_phone", False
                )),

            "linkedin_connected":
                int(signals.get(
                    "linkedin_connected", False
                )),

            # =====================
            # Skill Assessments
            # =====================

            "skill_assessment_avg":
                self.extract_skill_assessment_avg(signals),

            "skill_assessment_count":
                self.extract_skill_assessment_count(signals),

            # =====================
            # Activity Freshness
            # =====================

            "days_since_active":
                self.compute_days_since_active(signals),

            # =====================
            # Semantic Retrieval Text
            # (ENRICHED — title + headline + summary + skills + certs)
            # =====================

            "candidate_text": candidate_text
        }