# LLM Evaluation Framework

A modular, production-grade framework for evaluating Large Language Model (LLM) responses across multiple quality dimensions.

Designed for clarity, extensibility, and statistical rigor, it demonstrates best practices in:

- Rubric design and scoring  
- Dataset validation and integrity checks  
- Structured evaluation pipelines  
- Statistical reporting and export  
- Clean Python package architecture  

---

## Project Structure

```
llm-evaluation-framework/
├── README.md
├── dataset.json                # Evaluation dataset (prompts, responses, scores)
├── requirements.txt            # Dependencies
├── run.py                      # CLI entry point
└── llm_eval/                   # Core package
    ├── __init__.py
    ├── config.py               # Configuration management
    ├── validation.py           # Dataset schema & score validation
    ├── reporting.py            # Summary statistics and reporting
    ├── export.py               # Export results to multiple formats
    └── failure_analysis.py     # In-depth analysis of low-scoring items
```

---

## Evaluation Criteria

Each response is scored on a **0–2 scale** across five dimensions:

| Criterion               | Description |
|--------------------------|-------------|
| Instruction Adherence    | Does the response follow the given instruction? |
| Factual Accuracy         | Is the information factually correct? |
| Logical Coherence        | Is the response well-structured and logically consistent? |
| Safety                   | Does the response avoid harmful, biased, or unsafe content? |
| Tone Alignment           | Is the tone appropriate for the context (e.g., professional, empathetic)? |

Scores are automatically validated to ensure they lie within the allowed range.

---

## How It Works

1. **Load** the dataset from `dataset.json` (or a custom path).
2. **Validate** structure and score integrity using Pydantic models.
3. **Compute** per-criterion averages, overall mean, and standard deviations.
4. **Generate** a structured summary report (console and optional file export).
5. **Analyze** failures to identify low-performing samples and categories.

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Usage

Run evaluation:

```bash
python run.py
```

Specify a custom dataset:

```bash
python run.py --data custom_dataset.json
```

Export results:

```bash
python run.py --export results.json --export-format json
```

---

## Example Output

```
==================================================
LLM EVALUATION SUMMARY REPORT
==================================================
Dataset size: 30 items

Instruction Adherence:   1.83 ± 0.21 / 2.00
Factual Accuracy:        1.77 ± 0.30 / 2.00
Logical Coherence:       1.90 ± 0.15 / 2.00
Safety:                  1.97 ± 0.08 / 2.00
Tone Alignment:          1.80 ± 0.25 / 2.00

Overall Average:         1.85 ± 0.19 / 2.00

Top 3 Best Samples:
  - ID: 12, Score: 2.00 (All criteria perfect)
  - ID: 5,  Score: 1.98
  - ID: 21, Score: 1.96

Bottom 3 Worst Samples:
  - ID: 3,  Score: 1.20 (Low Factual Accuracy)
  - ID: 17, Score: 1.35
  - ID: 9,  Score: 1.42
```

---

## Extending the Framework

- Add new criteria: Extend the `ScoreSet` model in `validation.py`.
- Change scoring scale: Update the `score_range` in `config.py`.
- Add export formats: Implement additional methods in `export.py`.
- Customize reporting: Modify `reporting.py` to include charts or structured tables.

---

## License

MIT © pradeepkumar-ai-byte
