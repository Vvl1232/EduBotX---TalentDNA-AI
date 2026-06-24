# TalentDNA AI

AI-powered candidate ranking engine for the Redrob AI Hiring Challenge. Processes 100,000 candidate profiles against a job description to produce a ranked Top 100 shortlist using semantic retrieval, rule-based scoring, and integrity validation.

## Architecture

```
Raw Candidates (100K JSONL)
    │
    ▼
CandidateParser ─► CareerFeatureExtractor
    │
    ▼
EmbeddingEngine (BAAI/bge-small-en-v1.5)
    │
    ▼
FAISS Retrieval (Top 1000)
    │
    ▼
Scoring Engines (parallel):
    ├── RoleIntelligenceEngine
    ├── EvidenceMatchEngine
    ├── SignalEngine
    └── IntegrityEngine
    │
    ▼
HybridRanker ─► Top 100 CSV
```

## Pipeline Performance

- Full pipeline (cached): ~0.19 seconds
- Embedding generation (one-time): ~15 minutes
- FAISS index build (one-time): ~2 seconds

## Project Structure

```
TalentDNA_AI/
├── data/
│   └── raw/                       # Challenge dataset
│       ├── candidates.jsonl       # 100K candidate profiles
│       ├── candidate_schema.json
│       ├── job_description.docx
│       ├── sample_candidates.json
│       ├── sample_submission.csv
│       ├── validate_submission.py
│       └── (other challenge docs)
│
├── notebooks/
│   ├── 01_dataset_understanding.ipynb
│   ├── 02_candidate_parser.ipynb
│   ├── 03_jd_understanding.ipynb
│   ├── 06_ranking_engine.ipynb
│   ├── 07_explainability.ipynb
│   ├── 08_career_features.ipynb
│   ├── 09_jd_intent.ipynb
│   ├── 10_embeddings.ipynb
│   ├── 11_retrieval.ipynb
│   ├── 12_career_match.ipynb
│   ├── 13_signals.ipynb
│   ├── 14_end_to_end_pipeline.ipynb  # Main pipeline
│   ├── 15_role_intelligence.ipynb
│   ├── 16_evidence_match.ipynb
│   ├── candidate_embeddings.npy      # Pre-computed (146MB)
│   ├── candidate_index.faiss         # Pre-built index (146MB)
│   └── top100_submission_final.csv   # Final output
│
├── src/
│   ├── config.py                  # Centralized weights, keywords, thresholds
│   ├── parser.py                  # Candidate JSON → flat feature dict
│   ├── career_features.py         # Career history feature extraction
│   ├── jd_parser.py               # Job description parser
│   ├── jd_intent.py               # JD intent extraction
│   ├── embeddings.py              # Sentence transformer encoding
│   ├── retrieval.py               # FAISS similarity search
│   ├── evidence_match.py          # Keyword evidence scoring
│   ├── role_intelligence.py       # Role classification & scoring
│   ├── signals.py                 # Redrob platform signal scoring
│   ├── integrity_engine.py        # Honeypot & fraud detection
│   ├── ranker.py                  # Final hybrid ranking
│   ├── reason_generator.py        # Human-readable ranking reasons
│   └── explainability.py          # Explainability engine
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Scoring Components

| Component | Weight | Contribution | Purpose |
|---|---|---|---|
| **Role Intelligence** | 3.0 | ~68% | Title classification (high/medium/low value) |
| **Semantic Retrieval** | 114 | ~15% | Embedding similarity to JD intent |
| **Signal Engine** | 0.5 | ~7% | Platform engagement signals |
| **Evidence Match** | 2.0 | ~6% | Keyword evidence in profile text |
| **Experience Fit** | 20 | bonus | Years of experience alignment |
| **Location Fit** | 15 | bonus | Geographic preference match |
| **Freshness** | 10 | bonus | Profile activity recency |
| **Integrity** | multiplier | gate | Fraud detection (0 = disqualified) |

## Key Design Decisions

1. **Integrity as multiplicative gate**: Score × (integrity / 100). A candidate flagged as consulting-only or honeypot gets score 0, regardless of other features.

2. **Semantic weight calibrated via ablation**: Original semantic contribution was 2.38%. After sweep testing (5%–25%), 15% was selected as the optimal balance between hidden-trap detection and ranking stability (99% Top100 overlap).

3. **Rule-based over ML**: The challenge dataset contains synthetic traps (keyword-stuffed Marketing Managers, templated summaries). Deterministic rules detect these more reliably than learned models.

## Getting Started

```bash
pip install -r requirements.txt
```

Run the main pipeline notebook:
```
notebooks/14_end_to_end_pipeline.ipynb
```

## Submission

Output: `notebooks/top100_submission_final.csv`

Validated against: `data/raw/validate_submission.py`
