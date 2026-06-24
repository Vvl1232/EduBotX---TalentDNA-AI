class ReasonGenerator:

    def generate(
        self,
        candidate,
        role_score,
        evidence_score,
        signal_score
    ):

        reasons = []

        years_exp = candidate.get(
            "years_experience",
            0
        )

        title = candidate.get(
            "current_title",
            ""
        )

        reasons.append(
            f"{years_exp} years experience as {title}"
        )

        skills = candidate.get(
            "skill_names",
            []
        )

        retrieval_skills = [
            skill for skill in skills
            if skill in [
                "FAISS",
                "Pinecone",
                "Qdrant",
                "Information Retrieval",
                "Learning to Rank",
                "Embeddings",
                "Sentence Transformers"
            ]
        ]

        ml_skills = [
            skill for skill in skills
            if skill in [
                "Machine Learning",
                "MLOps",
                "Feature Engineering",
                "MLflow",
                "Python",
                "Spark",
                "Airflow"
            ]
        ]

        if retrieval_skills:
            reasons.append(
                "demonstrates retrieval and ranking expertise through "
                + ", ".join(retrieval_skills[:3])
            )

        elif ml_skills:
            reasons.append(
                "demonstrates applied ML experience through "
                + ", ".join(ml_skills[:3])
            )

        # Role alignment
        if role_score >= 120:
            reasons.append(
                "very strong alignment with the target AI ranking role"
            )

        elif role_score >= 100:
            reasons.append(
                "strong alignment with the target AI role"
            )

        elif role_score >= 40:
            reasons.append(
                "partially aligned engineering background"
            )

        # Evidence
        if evidence_score >= 20:
            reasons.append(
                "multiple signals of production AI/ML work"
            )

        elif evidence_score >= 12:
            reasons.append(
                "relevant AI and data engineering evidence"
            )

        elif evidence_score >= 8:
            reasons.append(
                "some relevant engineering evidence"
            )

        # Recruiter signals
        if signal_score >= 80:
            reasons.append(
                "excellent recruiter engagement signals"
            )

        elif signal_score >= 60:
            reasons.append(
                "strong recruiter engagement signals"
            )

        elif signal_score >= 40:
            reasons.append(
                "reasonable recruiter engagement signals"
            )

        # Experience fit
        if years_exp < 5:
            reasons.append(
                "slightly below ideal experience range"
            )

        elif years_exp > 12:
            reasons.append(
                "more senior than the target experience range"
            )

        return ". ".join(reasons) + "."