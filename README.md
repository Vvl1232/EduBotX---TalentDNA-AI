# TalentDNA AI

TalentDNA AI is an AI-powered candidate discovery and ranking system designed specifically for the Redrob AI Hiring Challenge. The system evaluates candidates against a target job description to produce a highly relevant, ranked Top 100 shortlist complete with explainable reasoning. 

To achieve scalable and accurate candidate assessment, TalentDNA AI uses a multi-stage pipeline encompassing semantic retrieval, role intelligence, evidence matching, recruiter signals, and integrity validation. This architecture allows the system to process massive datasets efficiently while providing deep, contextual insights into every candidate match.

---

# Live Demo

* **Streamlit Application:** [https://edubotx---talentdna-ai-3kvf2fpehcgrstgtqicpuh.streamlit.app](https://edubotx---talentdna-ai-3kvf2fpehcgrstgtqicpuh.streamlit.app)

* **GitHub Repository:** [https://github.com/Vvl1232/EduBotX---TalentDNA-AI](https://github.com/Vvl1232/EduBotX---TalentDNA-AI)

---

# System Architecture

```text
+-------------------+
|  100K Candidates  |
+-------------------+
          |
          v
+-------------------+
|  Embedding Index  |
+-------------------+
          |
          v
+-------------------+
|  FAISS Retrieval  |
+-------------------+
          |
          v
+-------------------+
| Candidate Parsing |
+-------------------+
          |
          v
+-------------------+
|  Career Feature   |
|    Extraction     |
+-------------------+
          |
          v
+-------------------+
|  Scoring Engines  |
+-------------------+
          |
          v
+-------------------+
|   Hybrid Ranker   |
+-------------------+
          |
          v
+-------------------+
|  Top 100 Output   |
+-------------------+
```

---

# Retrieval-First Architecture

The system searches the full 100,000-candidate pool.

Candidate embeddings and the FAISS index are precomputed once and stored as artifacts. 

At runtime:
1. The job description is embedded.
2. FAISS searches the entire candidate pool.
3. The most relevant candidates are retrieved.
4. Detailed scoring is performed only on retrieved candidates.

This optimization preserves ranking results while significantly reducing memory usage and runtime.

---

# Large Dataset & Precomputed Artifacts

The repository relies on the following key data files tracked via Git LFS:
* `data/raw/candidates.jsonl`
* `notebooks/candidate_embeddings.npy`
* `notebooks/candidate_index.faiss`

`candidates.jsonl` contains the challenge dataset. `candidate_embeddings.npy` contains precomputed embeddings for candidate profiles. `candidate_index.faiss` contains the FAISS vector index.

Git LFS is required because these files are several hundred megabytes in size. These files are generated from the challenge dataset and are included to avoid recomputing embeddings for every execution. 

The job description embedding is generated at runtime.

---

# Repository Structure

```text
.
├── .streamlit/
│   └── config.toml
├── data/
│   └── raw/
│       ├── candidates.jsonl
│       ├── job_description.docx
│       ├── submission_metadata.yaml
│       └── validate_submission.py
├── notebooks/
│   ├── 14_end_to_end_pipeline.ipynb
│   ├── candidate_embeddings.npy
│   └── candidate_index.faiss
├── src/
│   ├── career_features.py
│   ├── config.py
│   ├── embeddings.py
│   ├── evidence_match.py
│   ├── explainability.py
│   ├── integrity_engine.py
│   ├── jd_intent.py
│   ├── jd_parser.py
│   ├── parser.py
│   ├── ranker.py
│   ├── reason_generator.py
│   ├── retrieval.py
│   ├── role_intelligence.py
│   └── signals.py
├── app.py
├── rank.py
├── requirements.txt
├── runtime.txt
├── submission.csv
├── submission_metadata.yaml
└── TalentDNA AI - Methodology.pdf
```

---

# Local Reproduction Guide

**Step 1:**
```bash
git clone https://github.com/Vvl1232/EduBotX---TalentDNA-AI.git
cd EduBotX---TalentDNA-AI
```

**Step 2:**
```bash
git lfs install
git lfs pull
```
This downloads `candidates.jsonl`, `candidate_embeddings.npy`, and `candidate_index.faiss`.

**Step 3:**
```bash
pip install -r requirements.txt
```

**Step 4:**
Run ranking:
```bash
python rank.py --candidates data/raw/candidates.jsonl --jd data/raw/job_description.docx --out submission.csv
```

**Step 5:**
Validate:
```bash
python data/raw/validate_submission.py submission.csv
```
Expected output:
```
Submission format is VALID.
```

---

# Running the Streamlit Application

```bash
streamlit run app.py
```
The Streamlit demo uses the same ranking pipeline and retrieval system locally as it does in the cloud.

---

# Scoring Components

* **Semantic Retrieval:** Uses FAISS to perform vector similarity searches across candidate embeddings.
* **Role Intelligence:** Maps candidate skills and job titles directly to the core requirements of the job description.
* **Evidence Match:** Extracts and validates concrete professional experiences demonstrating required competencies.
* **Recruiter Signals:** Analyzes tenure, promotion trajectory, and overall career progression.
* **Integrity Engine:** Filters out profiles with anomalous data, such as impossible timelines or missing foundational details.
* **Explainability Engine:** Generates transparent, human-readable rationales for why each candidate was selected.

---

# Performance

* Full candidate search space: 100,000 candidates
* Retrieval engine: FAISS
* CPU-only execution
* Retrieval-first memory optimization
* Designed to execute well within challenge runtime requirements

---

# Deliverables

* Source Code
* Streamlit Application
* Methodology PDF
* `submission.csv`
* `submission_metadata.yaml`

---

# Team

**EduBotX**

* Vinit Limkar — Team Lead / AIML Engineer
* Sarah Khambatta — DevOps & Full Stack
* Shreyash Date — Full Stack Developer