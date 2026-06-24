import json
import argparse
import pandas as pd
import numpy as np
import faiss
from docx import Document

from src.parser import CandidateParser
from src.career_features import CareerFeatureExtractor
from src.embeddings import EmbeddingEngine
from src.retrieval import CandidateRetriever
from src.role_intelligence import RoleIntelligenceEngine
from src.evidence_match import EvidenceMatchEngine
from src.signals import SignalEngine
from src.integrity_engine import IntegrityEngine
from src.ranker import HybridRanker
from src.reason_generator import ReasonGenerator


def load_jd(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


def load_candidates(path):
    print("STAGE:1:START", flush=True)
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print("STAGE:1:END", flush=True)

    print("STAGE:2:START", flush=True)
    parser = CandidateParser()
    parsed_rows = []
    for line in lines:
        row = json.loads(line)
        parsed_rows.append((row, parser.parse(row)))
    print("STAGE:2:END", flush=True)

    print("STAGE:3:START", flush=True)
    career = CareerFeatureExtractor()
    candidates = []
    for row, candidate in parsed_rows:
        career_features = career.extract(
            row.get("career_history", [])
        )
        candidate.update(career_features)
        candidates.append(candidate)
    print("STAGE:3:END", flush=True)

    return candidates


def main():

    ap = argparse.ArgumentParser()

    ap.add_argument(
        "--candidates",
        required=True
    )

    ap.add_argument(
        "--jd",
        required=True
    )

    ap.add_argument(
        "--out",
        required=True
    )

    args = ap.parse_args()

    candidates = load_candidates(
        args.candidates
    )

    jd_text = load_jd(
        args.jd
    )

    print("STAGE:4:START", flush=True)
    embedding_engine = EmbeddingEngine()

    jd_embedding = embedding_engine.encode_text(
        jd_text
    )
    print("STAGE:4:END", flush=True)

    print("STAGE:5:START", flush=True)
    index = faiss.read_index(
        "notebooks/candidate_index.faiss"
    )

    scores, indices = index.search(
        np.array(
            [jd_embedding],
            dtype=np.float32
        ),
        1000
    )
    print("STAGE:5:END", flush=True)

    role_engine = RoleIntelligenceEngine()
    evidence_engine = EvidenceMatchEngine()
    signal_engine = SignalEngine()
    integrity_engine = IntegrityEngine()
    ranker = HybridRanker()
    reason_generator = ReasonGenerator()

    # Pre-select the retrieved candidates
    retrieved_candidates = []
    for pos, idx in enumerate(indices[0]):
        retrieved_candidates.append({
            "candidate": candidates[idx],
            "semantic_score": float(scores[0][pos])
        })

    print("STAGE:6:START", flush=True)
    for rc in retrieved_candidates:
        rc["evidence_score"] = evidence_engine.score(rc["candidate"])
    print("STAGE:6:END", flush=True)

    print("STAGE:7:START", flush=True)
    for rc in retrieved_candidates:
        rc["signal_score"] = signal_engine.score(rc["candidate"])
        rc["role_score"] = role_engine.score(rc["candidate"])
    print("STAGE:7:END", flush=True)

    print("STAGE:8:START", flush=True)
    for rc in retrieved_candidates:
        rc["integrity_score"] = integrity_engine.score(rc["candidate"])
    print("STAGE:8:END", flush=True)

    print("STAGE:9:START", flush=True)
    for rc in retrieved_candidates:
        rc["final_score"] = ranker.score(
            semantic_score=rc["semantic_score"],
            evidence_score=rc["evidence_score"],
            role_score=rc["role_score"],
            signal_score=rc["signal_score"],
            integrity_score=rc["integrity_score"],
            candidate=rc["candidate"]
        )

    retrieved_candidates.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    top100 = retrieved_candidates[:100]
    print("STAGE:9:END", flush=True)

    rows = []

    print("STAGE:10:START", flush=True)
    for rank, row in enumerate(
        top100,
        start=1
    ):

        candidate = row["candidate"]

        reasoning = reason_generator.generate(
            candidate,
            row["role_score"],
            row["evidence_score"],
            row["signal_score"]
        )

        rows.append({
            "candidate_id": candidate["candidate_id"],
            "rank": rank,
            "score": row["final_score"],
            "reasoning": reasoning
        })
    print("STAGE:10:END", flush=True)

    submission = pd.DataFrame(rows)

    assert len(submission) == 100
    assert submission["candidate_id"].nunique() == 100
    assert submission["rank"].tolist() == list(range(1, 101))

    print("STAGE:11:START", flush=True)
    submission.to_csv(
        args.out,
        index=False
    )
    print("STAGE:11:END", flush=True)


if __name__ == "__main__":
    main()