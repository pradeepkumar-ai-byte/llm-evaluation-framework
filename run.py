"""
CLI Orchestration Layer

Author: Pradeep Kumar

Entry point for LLM Evaluation Framework.
"""

import argparse
from pathlib import Path
import json

from llm_eval.config import Config
from llm_eval.validation import load_and_validate_dataset
from llm_eval.reporting import generate_report
from llm_eval.significance import independent_t_test
from llm_eval.agreement import compute_cohens_kappa
from llm_eval.benchmark import benchmark_against_reference
from llm_eval.advanced_drift import detect_kl_drift
from llm_eval.advanced_statistics import bootstrap_significance_test


def main():
    parser = argparse.ArgumentParser(
        description="LLM Evaluation Framework CLI"
    )

    parser.add_argument("--data", required=True, help="Dataset JSON file")
    parser.add_argument("--agreement", action="store_true")
    parser.add_argument("--significance", action="store_true")
    parser.add_argument("--benchmark", help="Reference dataset JSON file")
    parser.add_argument("--drift", help="Baseline dataset JSON file")
    parser.add_argument("--export", help="Export results to JSON file")

    args = parser.parse_args()

    config = Config()

    dataset = load_and_validate_dataset(Path(args.data), config)

    results = {}

    # Core report
    report = generate_report(dataset, config)
    print(report)
    results["report"] = report

    # Agreement
    if args.agreement:
        agreement = compute_cohens_kappa(dataset, config)
        print("\nCohen's Kappa:")
        print(agreement)
        results["agreement"] = agreement

    # Significance
    if args.significance:
        significance = independent_t_test(dataset, config)
        bootstrap = bootstrap_significance_test(dataset, config)

        print("\nT-Test Result:")
        print(significance)

        print("\nBootstrap Result:")
        print(bootstrap)

        results["significance"] = significance
        results["bootstrap"] = bootstrap

    # Benchmark
    if args.benchmark:
        reference_dataset = load_and_validate_dataset(
            Path(args.benchmark),
            config,
        )
        benchmark = benchmark_against_reference(
            dataset,
            reference_dataset,
            config,
        )

        print("\nBenchmark Result:")
        print(benchmark)

        results["benchmark"] = benchmark

    # Drift
    if args.drift:
        baseline_dataset = load_and_validate_dataset(
            Path(args.drift),
            config,
        )
        drift = detect_kl_drift(
            dataset,
            baseline_dataset,
            config,
        )

        print("\nDrift Detection:")
        print(drift)

        results["drift"] = drift

    # Export
    if args.export:
        with open(args.export, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

        print(f"\nResults exported to {args.export}")


if __name__ == "__main__":
    main()
