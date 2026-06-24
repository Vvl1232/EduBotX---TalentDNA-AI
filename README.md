# TalentDNA AI

TalentDNA AI is an intelligent candidate discovery and ranking engine developed for the Redrob AI Hiring Challenge. The system evaluates a pool of 100,000 candidate profiles against a target job description and produces a ranked Top 100 shortlist using semantic retrieval, role intelligence, evidence-based scoring, platform signals, integrity validation, and explainable AI reasoning.

---

# Key Features

* Semantic Candidate Retrieval using FAISS
* Job Description Intent Understanding
* Role Intelligence Scoring
* Evidence-Based Skill Matching
* Candidate Integrity Validation
* Explainable Ranking Reasons
* Retrieval-First Memory Optimized Architecture
* Interactive Streamlit Evaluation Dashboard

---

# System Architecture

```text
100K Candidate Dataset
        │
        ▼
Embedding Index (FAISS)
        │
        ▼
JD Understanding & Intent Extraction
        │
        ▼
Semantic Retrieval (Top 1000)
        │
        ▼
Candidate Parsing & Career Feature Extraction
        │
        ▼
Scoring Engines
    ├── Role Intelligence
    ├── Evidence Match
    ├── Platform Signals
    └── Integrity Engine
        │
        ▼
Hybrid Ranking Engine
        │
        ▼
Top 100 Candidates
        │
        ▼
Explainability & Candidate Insights
```

---

# Retrieval-First Optimization

TalentDNA AI uses a retrieval-first architecture for scalability.

Instead of parsing and processing all 100,000 candidates before ranking, the system:

1. Searches the complete 100K candidate pool using a FAISS vector index.
2. Retrieves the most relevant candidate subset.
3. Performs detailed feature extraction and scoring only on retrieved candidates.
4. Produces identical ranking results while significantly reducing memory consumption and execution time.

This optimization preserves ranking correctness while enabling efficient deployment in constrained environments.

---

# Project Structure

```text
TalentDNA_AI/

├── .streamlit/
│
├── data/
│   └── raw/
│       ├── candidates.jsonl
│       ├── candidate_schema.json
│       ├── job_description.docx
│       ├── redrob_signals_doc.docx
│       ├── sample_candidates.json
│       ├── sample_submission.csv
│       ├── submission_metadata.yaml
│       ├── submission_spec.docx
│       └── validate_submission.py
│
├── notebooks/
│   ├── candidate_embeddings.npy
│   └── candidate_index.faiss
│
├── src/
│   ├── parser.py
│   ├── career_features.py
│   ├── jd_parser.py
│   ├── jd_intent.py
│   ├── embeddings.py
│   ├── retrieval.py
│   ├── evidence_match.py
│   ├── role_intelligence.py
│   ├── signals.py
│   ├── integrity_engine.py
│   ├── ranker.py
│   ├── reason_generator.py
│   ├── explainability.py
│   └── config.py
│
├── app.py
├── rank.py
├── requirements.txt
├── runtime.txt
├── submission.csv
├── submission_metadata.yaml
├── TalentDNA AI - Methodology.pdf
└── README.md
```

---

# Scoring Components

| Component             | Purpose                                            |
| --------------------- | -------------------------------------------------- |
| Semantic Retrieval    | Candidate relevance to job description             |
| Role Intelligence     | Role and title alignment                           |
| Evidence Match        | Verified skill and keyword evidence                |
| Platform Signals      | Candidate engagement indicators                    |
| Integrity Engine      | Fraud, honeypot, and low-quality profile detection |
| Explainability Engine | Human-readable ranking justification               |

---

# Installation

```bash
pip install -r requirements.txt
```

---

# Running the Ranking Pipeline

```bash
python rank.py \
--candidates data/raw/candidates.jsonl \
--jd job_description.docx \
--out submission.csv
```

---

# Running the Streamlit Application

```bash
streamlit run app.py
```

---

# Output

The system generates:

```text
submission.csv
```

containing the final ranked Top 100 candidates.

Validation can be performed using:

```bash
python data/raw/validate_submission.py submission.csv
```

---

# Deliverables

* Source Code
* Streamlit Application - https://edubotx---talentdna-ai-3kvf2fpehcgrstgtqicpuh.streamlit.app/
* Methodology Document
* Submission CSV
* Submission Metadata
* Reproducible Ranking Pipeline

---

# Team

EduBotX

Redrob AI Hiring Challenge Submission
