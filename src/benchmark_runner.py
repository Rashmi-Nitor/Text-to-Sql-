import json
from collections import Counter
from pathlib import Path

if __package__:
    from .evaluator import execute_query
    from .sql_generator import generate_sql
    from .validator import validate
else:
    from evaluator import execute_query
    from sql_generator import generate_sql
    from validator import validate


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_benchmark() -> dict[str, int | float]:
    """Run the benchmark cases and report execution accuracy."""
    cases_path = PROJECT_ROOT / "benchmark" / "test_cases.json"
    with cases_path.open("r", encoding="utf-8") as cases_file:
        test_cases = json.load(cases_file)

    total_tests = len(test_cases)
    passed_tests = 0
    benchmark_results = []

    print("\n==============================")
    print("STARTING BENCHMARK")
    print("==============================\n")

    for idx, test in enumerate(test_cases, start=1):
        question = test["question"]
        gold_sql = test["gold_sql"]

        print(f"\n[{idx}/{total_tests}]")
        print(f"Question: {question}")

        try:
            generated_sql = generate_sql(question)

            print("\nGenerated SQL:")
            print(generated_sql)

            is_valid, validation_msg = validate(generated_sql)
            if not is_valid:
                print("VALIDATION FAILED")
                print(validation_msg)
                benchmark_results.append(
                    {
                        "question": question,
                        "gold_sql": gold_sql,
                        "generated_sql": generated_sql,
                        "status": "VALIDATION_FAILED",
                        "details": validation_msg,
                    }
                )
                continue

            gold_result = execute_query(gold_sql)
            generated_result = execute_query(generated_sql)

            if Counter(gold_result) == Counter(generated_result):
                passed_tests += 1
                print("PASS")
                benchmark_results.append(
                    {
                        "question": question,
                        "gold_sql": gold_sql,
                        "generated_sql": generated_sql,
                        "status": "PASS",
                    }
                )
            else:
                print("FAIL")
                print(f"Expected Result: {gold_result}")
                print(f"Generated Result: {generated_result}")
                benchmark_results.append(
                    {
                        "question": question,
                        "gold_sql": gold_sql,
                        "generated_sql": generated_sql,
                        "status": "FAIL",
                        "gold_result": str(gold_result),
                        "generated_result": str(generated_result),
                    }
                )
        except Exception as error:
            print(f"ERROR: {error}")
            benchmark_results.append(
                {
                    "question": question,
                    "gold_sql": gold_sql,
                    "status": "ERROR",
                    "details": str(error),
                }
            )

    accuracy = passed_tests / total_tests * 100 if total_tests else 0
    summary: dict[str, int | float] = {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": total_tests - passed_tests,
        "accuracy": round(accuracy, 2),
    }

    print("\n==============================")
    print("BENCHMARK COMPLETE")
    print("==============================")
    print(f"Passed : {passed_tests}/{total_tests}")
    print(f"Accuracy : {accuracy:.2f}%")

    output_path = PROJECT_ROOT / "outputs" / "results.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(
            {"summary": summary, "results": benchmark_results},
            output_file,
            indent=4,
        )

    print(f"\nResults saved to: {output_path}")
    return summary


if __name__ == "__main__":
    run_benchmark()
