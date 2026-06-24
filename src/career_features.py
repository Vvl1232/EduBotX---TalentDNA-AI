class CareerFeatureExtractor:

    def __init__(self):
        pass

    def get_current_role(self, history):

        for job in history:

            if job.get("is_current", False):
                return job.get("title", "")

        return ""

    def get_total_duration(self, history):

        total = 0

        for job in history:

            total += job.get(
                "duration_months",
                0
            )

        return total

    def get_num_companies(self, history):

        return len(history)

    def get_career_companies(self, history):
        """
        Extract ordered list of all company names from career history.
        Required by IntegrityEngine for consulting-only detection.
        Without this, IntegrityEngine silently falls back to
        current_company only, missing prior consulting history.
        """
        return [
            job.get("company", "")
            for job in history
            if job.get("company")
        ]

    def get_industries(self, history):

        return list(
            set(
                [
                    job.get(
                        "industry",
                        ""
                    )
                    for job in history
                ]
            )
        )

    def get_job_titles(self, history):

        return [
            job.get(
                "title",
                ""
            )
            for job in history
        ]

    def build_experience_text(
        self,
        history
    ):

        text_parts = []

        for job in history:

            title = job.get(
                "title",
                ""
            )

            industry = job.get(
                "industry",
                ""
            )

            desc = job.get(
                "description",
                ""
            )

            text_parts.append(
                f"{title} {industry} {desc}"
            )

        return " ".join(
            text_parts
        )

    def career_growth_score(
        self,
        history
    ):

        titles = [
            job.get(
                "title",
                ""
            ).lower()
            for job in history
        ]

        senior_keywords = [
            "lead",
            "senior",
            "principal",
            "manager",
            "head",
            "director"
        ]

        score = 0

        for title in titles:

            if any(
                word in title
                for word in senior_keywords
            ):
                score += 1

        return score

    def extract(
        self,
        career_history
    ):

        return {

            "current_role":
                self.get_current_role(
                    career_history
                ),

            "total_duration_months":
                self.get_total_duration(
                    career_history
                ),

            "num_companies":
                self.get_num_companies(
                    career_history
                ),

            "industries":
                self.get_industries(
                    career_history
                ),

            "job_titles":
                self.get_job_titles(
                    career_history
                ),

            "experience_text":
                self.build_experience_text(
                    career_history
                ),

            "career_growth_score":
                self.career_growth_score(
                    career_history
                ),

            # Full company name list - required by IntegrityEngine
            # for consulting-only career detection.
            # Bug: was previously missing, causing IntegrityEngine
            # to fall back to current_company only.
            "career_companies":
                self.get_career_companies(
                    career_history
                )
        }