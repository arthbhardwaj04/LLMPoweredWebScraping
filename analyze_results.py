
import pandas as pd
import pathlib
import math
import yaml

def main():
    merged_file = pathlib.Path("outputs/nologin_validation_results_merged.csv")
    csv_output = pathlib.Path("outputs/average_summary.csv")
    yaml_output = pathlib.Path("outputs/average_summary.yaml")

    if not merged_file.exists():
        print(f"Error: {merged_file} not found. Run with --engine both first.")
        return

    # Load data
    df = pd.read_csv(merged_file)
    df["TimeTaken"] = pd.to_numeric(df["TimeTaken"], errors="coerce")
    df["Success"] = df["Success/Fail"].str.lower().eq("success")

    run_size = 32  # number of sites per run per engine
    engines = df["Engine"].unique()
    rows = []

    for engine in engines:
        eng_df = df[df["Engine"] == engine].reset_index(drop=True)
        num_runs = math.ceil(len(eng_df) / run_size)

        for run in range(num_runs):
            start = run * run_size
            end = (run + 1) * run_size
            run_df = eng_df.iloc[start:end]

            if len(run_df) == 0:
                continue

            avg_time = run_df["TimeTaken"].mean()
            success_rate = run_df["Success"].mean() * 100 if len(run_df) > 0 else 0

            rows.append({
                "Engine": engine,
                "Run": f"Run{run+1}",
                "SampleSize": len(run_df),
                "AverageTimeTaken": round(avg_time, 2),
                "SuccessRate": round(success_rate, 1)
            })

        # Overall averages for this engine
        avg_time = eng_df["TimeTaken"].mean()
        success_rate = eng_df["Success"].mean() * 100
        rows.append({
            "Engine": engine,
            "Run": "Overall",
            "SampleSize": len(eng_df),
            "AverageTimeTaken": round(avg_time, 2),
            "SuccessRate": round(success_rate, 1)
        })

    summary = pd.DataFrame(rows)

    # Print results
    print("📊 Metrics per Engine and Run")
    for _, row in summary.iterrows():
        print(f"- {row['Engine']} {row['Run']} → Sample size: {row['SampleSize']} | "
              f"Avg time: {row['AverageTimeTaken']} sec | Success rate: {row['SuccessRate']}%")

    # Save CSV
    csv_output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(csv_output, index=False)
    print(f"Summary saved to {csv_output}")

    # Save YAML
    yaml_data = summary.to_dict(orient="records")
    with open(yaml_output, "w", encoding="utf-8") as yf:
        yaml.safe_dump(yaml_data, yf, sort_keys=False)
    print(f"Summary saved to {yaml_output}")

if __name__ == "__main__":
    main()
