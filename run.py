"""
CLI Orchestration Layer

Author: Pradeep Kumar

Entry point for LLM Evaluation Framework.
"""

import argparse
from pathlib import Path

from llm_eval.config import Config
from llm_eval.validation import load_and_validate_dataset
from llm_eval.reporting import generate_report
from llm_eval.significance import independent_t_test
from llm_eval.agreement import compute_cohens_kappa
from llm_eval.benchmark import benchmark_against_reference
from llm_eval.advanced_drift import detect_kl_drift
from llm_eval.advanced_statistics import bootstrap_significance_test
from llm_eval.export import export_results


def main():
    parser = argparse.ArgumentParser(
        description="LLM Evaluation Framework CLI"
    )

    parser.add_argument(
        "--data",
        required=True,
        help="Path to evaluation dataset JSON file",
    )

    parser.add_argument(
        "--agreement",
        action="store_true",
        help="Compute inter-rater agreement (Cohen's Kappa)",
    )

    parser.add_argument(
        "--significance",
        action="store_true",
        help="Run independent t-test and bootstrap significance",
    )

    parser.add_argument(
        "--benchmark",
        help="Path to reference dataset JSON file",
    )

    parser.add_argument(
        "--drift",
        help="Path to baseline dataset JSON file",
    )

    parser.add_argument(
        "--export",
        help="Export results to JSON file",
    )

    args = parser.parse_args()

    config = Config()

    # Load main dataset
    dataset = load_and_validate_dataset(
        Path(args.data),
        config,
    )

    results = {}

    # Generate core report
    report = generate_report(dataset, config)
    print(report)
    results["report"] = report

    # Agreement analysis
    if args.agreement:
        agreement = compute_cohens_kappa(dataset, config)
        print("\nCohen's Kappa:")
        print(agreement)
        results["agreement"] = agreement

    # Significance testing
    if args.significance:
        t_test_result = independent_t_test(dataset, config)
        bootstrap_result = bootstrap_significance_test(dataset, config)

        print("\nT-Test Result:")
        print(t_test_result)

        print("\nBootstrap Result:")
        print(bootstrap_result)

        results["significance"] = t_test_result
        results["bootstrap"] = bootstrap_result

    # Benchmark comparison
    if args.benchmark:
        reference_dataset = load_and_validate_dataset(
            Path(args.benchmark),
            config,
        )

        benchmark_result = benchmark_against_reference(
            dataset,
            reference_dataset,
            config,
        )

        print("\nBenchmark Result:")
        print(benchmark_result)

        results["benchmark"] = benchmark_result

    # Drift detection
    if args.drift:
        baseline_dataset = load_and_validate_dataset(
            Path(args.drift),
            config,
        )

        drift_result = detect_kl_drift(
            dataset,
            baseline_dataset,
            config,
        )

        print("\nDrift Detection:")
        print(drift_result)

        results["drift"] = drift_result

    # Export results
    if args.export:
        export_results(results, Path(args.export))
        print(f"\nResults exported to {args.export}")


if __name__ == "__main__":
    main()
