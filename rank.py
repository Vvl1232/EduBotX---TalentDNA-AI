import json
import argparse
import pandas as pd
import numpy as np
import faiss
from docx import Document
import time
import tracemalloc
import traceback
import sys

class PipelineStage:
    def __init__(self, stage_num):
        self.stage_num = stage_num

    def __enter__(self):
        self.start_time = time.time()
        tracemalloc.start()
        self.mem_before, _ = tracemalloc.get_traced_memory()
        print(f"STAGE:{self.stage_num}:START", flush=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        mem_after, _ = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        elapsed = time.time() - self.start_time
        mem_before_mb = self.mem_before / (1024 * 1024)
        mem_after_mb = mem_after / (1024 * 1024)
        mem_diff = mem_after_mb - mem_before_mb

        print(f"LOG:Stage {self.stage_num} executed in {elapsed:.2f}s | Mem Before: {mem_before_mb:.2f}MB | Mem After: {mem_after_mb:.2f}MB | Diff: {mem_diff:+.2f}MB", flush=True)

        if exc_type is not None:
            err_type = exc_type.__name__
            err_msg = str(exc_val)
            print(f"STAGE:{self.stage_num}:ERROR:{err_type}:{err_msg}", flush=True)
            tb_str = "".join(traceback.format_exception(exc_type, exc_val, exc_tb))
            tb_encoded = tb_str.replace('
', '<br>').replace('', '')
            print(f"TRACEBACK:{tb_encoded}", flush=True)
            sys.exit(1)

        print(f"STAGE:{self.stage_num}:END", flush=True)
        return False


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
    with PipelineStage(1):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        print(f"LOG:Loaded {len(lines)} raw candidate lines", flush=True)

    with PipelineStage(2):
        parser = CandidateParser()
        parsed_rows = []
        for line in lines:
            row = json.loads(line)
            parsed_rows.append((row, parser.parse(row)))
        print(f"LOG:Parsed {len(parsed_rows)} candidate profiles", flush=True)

    with PipelineStage(3):
        career = CareerFeatureExtractor()
        candidates = []
        for row, candidate in parsed_rows:
            career_features = career.extract(
                row.get("career_history", [])
            )
            candidate.update(career_features)
            candidates.append(candidate)
        print(f"LOG:Extracted career features for {len(candidates)} candidates", flush=True)

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

    with PipelineStage(4):
        embedding_engine = EmbeddingEngine()
        jd_embedding = embedding_engine.encode_text(
            jd_text
        )

    with PipelineStage(5):
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
        print(f"LOG:Retrieved {len(indices[0])} candidates via FAISS", flush=True)

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

    with PipelineStage(6):
        for rc in retrieved_candidates:
            rc["evidence_score"] = evidence_engine.score(rc["candidate"])

    with PipelineStage(7):
        for rc in retrieved_candidates:
            rc["signal_score"] = signal_engine.score(rc["candidate"])
            rc["role_score"] = role_engine.score(rc["candidate"])

    with PipelineStage(8):
        for rc in retrieved_candidates:
            rc["integrity_score"] = integrity_engine.score(rc["candidate"])

    with PipelineStage(9):
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

    rows = []

    with PipelineStage(10):
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

    submission = pd.DataFrame(rows)

    assert len(submission) == 100
    assert submission["candidate_id"].nunique() == 100
    assert submission["rank"].tolist() == list(range(1, 101))

    with PipelineStage(11):
        submission.to_csv(
            args.out,
            index=False
        )


if __name__ == "__main__":
    main()