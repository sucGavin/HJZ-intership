from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from run_dispatch_simulation import RESULTS_DIR, SEED, run_de, run_pso


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "simulated_dispatch_data.csv"
OUTPUT_CSV = RESULTS_DIR / "multi_day_runtime_comparison.csv"
OUTPUT_MD = RESULTS_DIR / "multi_day_runtime_summary.md"
POINTS_PER_DAY = 96
EXPECTED_DAYS = 7


def load_dispatch_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["time"])
    expected_points = EXPECTED_DAYS * POINTS_PER_DAY
    if len(df) != expected_points:
        raise ValueError(f"{DATA_PATH} should contain {expected_points} rows, got {len(df)}")
    return df


def run_multi_day_runtime_comparison() -> pd.DataFrame:
    RESULTS_DIR.mkdir(exist_ok=True)
    df = load_dispatch_data()
    rows = []
    daily_samples = list(df.groupby(df["time"].dt.normalize(), sort=True))

    if len(daily_samples) != EXPECTED_DAYS:
        raise ValueError(f"{DATA_PATH} should contain {EXPECTED_DAYS} natural days, got {len(daily_samples)}")

    for day_idx, (_, sample) in enumerate(daily_samples, start=1):
        sample = sample.reset_index(drop=True)
        if len(sample) != POINTS_PER_DAY:
            raise ValueError(f"Sample {day_idx} should contain {POINTS_PER_DAY} rows")

        pso_run = run_pso(sample, SEED + 100)
        de_run = run_de(sample, SEED + 200)
        pso_time = float(pso_run["runtime"])
        de_time = float(de_run["runtime"])

        rows.append(
            {
                "样本编号": day_idx,
                "起始时间": sample["time"].iloc[0].strftime("%Y-%m-%d %H:%M:%S"),
                "结束时间": sample["time"].iloc[-1].strftime("%Y-%m-%d %H:%M:%S"),
                "PSO运行时间/s": pso_time,
                "DE运行时间/s": de_time,
                "DE/PSO时间比": de_time / pso_time if pso_time > 0 else np.nan,
            }
        )

    out = pd.DataFrame(rows)
    numeric_cols = ["PSO运行时间/s", "DE运行时间/s", "DE/PSO时间比"]
    out[numeric_cols] = out[numeric_cols].astype(float).round(4)
    out.to_csv(OUTPUT_CSV, index=False)
    write_summary(out)
    return out


def write_summary(comparison: pd.DataFrame) -> Path:
    pso_mean = float(comparison["PSO运行时间/s"].mean())
    de_mean = float(comparison["DE运行时间/s"].mean())
    ratio_mean = float(comparison["DE/PSO时间比"].mean())
    conclusion = (
        f"在 7 个自然日样本、相同目标函数与算法参数下，DE 的平均运行时间约为 PSO 的 {ratio_mean:.4f} 倍。"
    )

    text = f"""# 多典型日运行时间对比实验

## 实验口径

读取 `data/simulated_dispatch_data.csv`，按自然日切分为 7 个样本，每个样本 96 个 15 min 调度点；每个样本分别运行 PSO 和 DE，并仅统计算法运行时间。

## 汇总结果

- PSO 平均运行时间/s：{pso_mean:.4f}
- DE 平均运行时间/s：{de_mean:.4f}
- DE 相对 PSO 的平均时间倍数：{ratio_mean:.4f}

## 客观结论

{conclusion}
"""
    OUTPUT_MD.write_text(text, encoding="utf-8")
    return OUTPUT_MD


def validate_outputs(comparison: pd.DataFrame) -> dict[str, bool]:
    expected_cols = [
        "样本编号",
        "起始时间",
        "结束时间",
        "PSO运行时间/s",
        "DE运行时间/s",
        "DE/PSO时间比",
    ]
    return {
        "rows_are_7": len(comparison) == EXPECTED_DAYS,
        "columns_match": list(comparison.columns) == expected_cols,
        "sample_numbers_match": comparison["样本编号"].tolist() == list(range(1, EXPECTED_DAYS + 1)),
        "runtime_positive": bool((comparison[["PSO运行时间/s", "DE运行时间/s"]] > 0).all().all()),
        "ratio_matches": bool(
            np.allclose(
                comparison["DE/PSO时间比"],
                comparison["DE运行时间/s"] / comparison["PSO运行时间/s"],
                rtol=1e-4,
                atol=1e-4,
            )
        ),
        "csv_exists": OUTPUT_CSV.exists(),
        "summary_exists": OUTPUT_MD.exists(),
    }


def main():
    comparison = run_multi_day_runtime_comparison()
    checks = validate_outputs(comparison)
    print("MULTI_DAY_RUNTIME_COMPARISON:", OUTPUT_CSV)
    print("MULTI_DAY_RUNTIME_SUMMARY:", OUTPUT_MD)
    print(comparison.to_string(index=False))
    print("BASIC_CHECKS:", checks)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
