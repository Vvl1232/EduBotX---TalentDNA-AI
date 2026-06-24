"""
TalentDNA AI - retrieval Module
"""

import faiss
import numpy as np


class CandidateRetriever:

    def __init__(self):

        self.index = None

        self.candidate_ids = []

    def build_index(
        self,
        embeddings,
        candidate_ids
    ):

        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(
            embeddings
        )

        self.candidate_ids = candidate_ids

    def search(
        self,
        query_embedding,
        top_k=100
    ):

        query_embedding = np.array(
            [query_embedding],
            dtype=np.float32
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            results.append({

                "candidate_id":
                    self.candidate_ids[idx],

                "semantic_score":
                    float(score)
            })

        return results