"""
Convert Excel to CSV for DBT seeds
"""
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
EXCEL_PATH = PROJECT_ROOT / 'data' / 'Telco_customer_churn.xlsx'
CSV_PATH = PROJECT_ROOT / 'dbt_project' / 'seeds' / 'Telco_customer_churn.csv'

print("📊 Converting Excel to CSV...")
print(f"Reading: {EXCEL_PATH}")

# Read Excel
df = pd.read_excel(EXCEL_PATH)
print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")

# Clean data - handle empty values in numeric columns
print("\n🧹 Cleaning data...")

# Fix Total Charges - replace spaces/empty with 0
if 'Total Charges' in df.columns:
    df['Total Charges'] = pd.to_numeric(df['Total Charges'], errors='coerce').fillna(0)
    print(f"  ✅ Fixed Total Charges (found {df['Total Charges'].isna().sum()} nulls)")

# Check for other problematic columns
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
for col in numeric_cols:
    nulls = df[col].isna().sum()
    if nulls > 0:
        df[col] = df[col].fillna(0)
        print(f"  ✅ Fixed {col} ({nulls} nulls)")

# Save as CSV
CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(CSV_PATH, index=False)

print(f"✅ Saved to: {CSV_PATH}")
print("\nNext steps:")
print("  cd dbt_project")
print("  dbt seed")
print("  dbt run")