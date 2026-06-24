"""
TalentDNA AI - embeddings Module
"""

from sentence_transformers import SentenceTransformer


class EmbeddingEngine:

    def __init__(self):

        from src.config import EMBEDDING_MODEL

        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    def encode_text(
        self,
        text
    ):

        return self.model.encode(
            text,
            normalize_embeddings=True
        )

    def encode_texts(
        self,
        texts,
        batch_size=256
    ):

        return self.model.encode(

            texts,

            batch_size=batch_size,

            show_progress_bar=True,

            normalize_embeddings=True
        )

    def encode_candidate(
        self,
        candidate
    ):

        text = candidate.get(
            "candidate_text",
            ""
        )

        return self.encode_text(
            text
        )

    def encode_candidates(
        self,
        candidates,
        batch_size=256
    ):

        texts = [

            candidate.get(
                "candidate_text",
                ""
            )

            for candidate in candidates
        ]

        return self.encode_texts(

            texts,

            batch_size=batch_size
        )

    def encode_jd(
        self,
        parsed_jd
    ):

        from src.config import RETRIEVAL_QUERY

        return self.encode_text(
            RETRIEVAL_QUERY
        )