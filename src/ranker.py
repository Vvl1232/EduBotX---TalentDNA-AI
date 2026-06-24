"""
TalentDNA AI - ranker Module
"""
from src.config import (
    RANKING_WEIGHTS,
    EXPERIENCE_RANGE,
    PREFERRED_LOCATIONS
)

class HybridRanker:

    def __init__(self):
        self.weights = RANKING_WEIGHTS
        self.exp_range = EXPERIENCE_RANGE
        self.pref_locations = PREFERRED_LOCATIONS

    def score(
        self,
        semantic_score,
        evidence_score,
        role_score,
        signal_score,
        integrity_score,
        candidate
    ):
        
        # 1. Experience Fit (0.0 to 1.0)
        years = candidate.get("years_experience", 0)
        exp_fit = 0.0
        if self.exp_range["ideal_min"] <= years <= self.exp_range["ideal_max"]:
            exp_fit = 1.0
        elif self.exp_range["hard_min"] <= years <= self.exp_range["hard_max"]:
            exp_fit = 0.5
            
        # 2. Location Fit (0.0 to 1.0)
        location = candidate.get("location", "").lower()
        loc_fit = 0.0
        if any(loc in location for loc in self.pref_locations):
            loc_fit = 1.0
            
        # 3. Freshness (0.0 to 1.0)
        days = candidate.get("days_since_active", 999)
        freshness_fit = 0.0
        if days <= 30:
            freshness_fit = 1.0
        elif days <= 90:
            freshness_fit = 0.5

        # Base components
        base_score = (
            semantic_score * self.weights["semantic"] +
            evidence_score * self.weights["evidence"] +
            role_score * self.weights["role"] +
            signal_score * self.weights["signal"] +
            exp_fit * self.weights["experience_fit"] +
            loc_fit * self.weights["location_fit"] +
            freshness_fit * self.weights["freshness"]
        )

        # Integrity acts as a multiplier (0 to 100 -> 0.0 to 1.0)
        integrity_multiplier = max(0, min(100, integrity_score)) / 100.0
        
        final_score = base_score * integrity_multiplier

        return round(final_score, 2)