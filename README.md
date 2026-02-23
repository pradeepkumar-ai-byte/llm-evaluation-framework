# 🚀 LLM Evaluation Framework

A modular, production-style evaluation framework for assessing Large Language Model (LLM) responses across multiple quality dimensions.

This project demonstrates practical skills in:

- Rubric design
- Dataset validation
- Structured evaluation pipelines
- Statistical reporting
- Clean Python package architecture

---

## 📂 Project Structure
llm-evaluation-framework/ │ ├── README.md ├── dataset.json ├── requirements.txt ├── run.py │ └── llm_eval/ ├── init.py ├── config.py ├── validation.py └── reporting.py

---

## 📊 Evaluation Criteria

Each response is scored from **0 to 2** across five dimensions:

1. Instruction Adherence  
2. Factual Accuracy  
3. Logical Coherence  
4. Safety  
5. Tone Alignment  

Scores are validated automatically before reporting.

---

## ⚙️ How It Works

1. Loads dataset from `dataset.json`
2. Validates structure and scoring integrity
3. Computes per-criterion averages
4. Generates professional summary report
5. Ranks best and worst performing samples

---

## ▶️ Usage

Run locally:

```bash
python run.py
Or specify dataset:
Bash
python run.py --data dataset.json

📈 Example Output

============================================================
LLM EVALUATION SUMMARY REPORT
============================================================
Dataset size: 30 items

Instruction Adherence        : 1.83 / 2.00
Factual Accuracy             : 1.77 / 2.00
Logical Coherence            : 1.90 / 2.00
Safety                       : 1.97 / 2.00
Tone Alignment               : 1.80 / 2.00
------------------------------------------------------------
Overall Average              : 1.85 / 2.00
============================================================
