#!/usr/bin/env python3
# csv_clean_and_summary.py
# Reads a CSV, basic cleaning, and outputs cleaned CSV + summary report (JSON).

import pandas as pd
import json
import sys

INPUT = "sample_input.csv"   # replace with your file
CLEANED = "cleaned_output.csv"
SUMMARY = "summary_report.json"

def clean_df(df):
    # Example cleaning steps
    df = df.copy()
    # Trim whitespace from string columns
    for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].str.strip()
    # Fill numeric NaNs with 0
    for c in df.select_dtypes(include=["int64", "float64"]).columns:
        df[c] = df[c].fillna(0)
    # Drop duplicate rows
    df = df.drop_duplicates()
    return df

def summarize(df):
    summary = {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "missing_values_per_column": df.isnull().sum().to_dict(),
        "numeric_stats": df.select_dtypes(include=["int64","float64"]).describe().to_dict()
    }
    return summary

def main(input_path=INPUT):
    df = pd.read_csv(input_path)
    cleaned = clean_df(df)
    cleaned.to_csv(CLEANED, index=False)
    report = summarize(cleaned)
    with open(SUMMARY, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Cleaned CSV saved to {CLEANED}")
    print(f"Summary report saved to {SUMMARY}")

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else INPUT
    main(arg)
