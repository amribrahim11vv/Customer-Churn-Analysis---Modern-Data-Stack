"""
Train ML model using data from DuckDB
"""
import duckdb
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from imblearn.over_sampling import SMOTE
import joblib

PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / 'data' / 'churn.duckdb'
MODEL_DIR = PROJECT_ROOT / 'models'

print("🤖 Training Churn Prediction Model")
print("=" * 60)

# Connect to DuckDB
print("\n📊 Loading data from DuckDB...")
conn = duckdb.connect(str(DB_PATH))

# Load data
df = conn.execute("""
    SELECT * FROM main_marts.fct_customer_churn
""").df()

print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")

# Prepare features and target
print("\n🔧 Preparing features...")

# Drop leakage columns and non-features
exclude_cols = [
    'customer_id', 
    'Churn Label',
    'Churn Value',    # LEAKAGE!
    'Churn Score',    # LEAKAGE!
    'Churn Reason'    # LEAKAGE!
]
feature_cols = [col for col in df.columns if col not in exclude_cols]

X = df[feature_cols]
y = df['Churn Label']

print(f"Features: {len(feature_cols)}")

# Encode categorical columns BEFORE split
categorical_cols = X.select_dtypes(include=['object']).columns
if len(categorical_cols) > 0:
    print(f"\n🔤 Encoding {len(categorical_cols)} categorical columns...")
    X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
    print(f"After encoding: {X.shape[1]} features")

print(f"\nTarget distribution:")
print(y.value_counts())

# Train-test split
print("\n📊 Splitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Train: {len(X_train)} | Test: {len(X_test)}")

# Handle class imbalance with SMOTE
print("\n⚖️ Handling class imbalance (SMOTE)...")
print(f"Before: {dict(zip(*np.unique(y_train, return_counts=True)))}")

smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

print(f"After: {dict(zip(*np.unique(y_train_balanced, return_counts=True)))}")

# Feature scaling
print("\n📏 Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_balanced)
X_test_scaled = scaler.transform(X_test)

# Train models
print("\n🏋️ Training models...")
models = {}
results = []

# 1. Logistic Regression
print("  1️⃣ Logistic Regression...")
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_scaled, y_train_balanced)
models['Logistic Regression'] = lr

# 2. Random Forest
print("  2️⃣ Random Forest...")
rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
rf.fit(X_train_scaled, y_train_balanced)
models['Random Forest'] = rf

# 3. XGBoost
print("  3️⃣ XGBoost...")
xgb = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, 
                    random_state=42, eval_metric='logloss')
xgb.fit(X_train_scaled, y_train_balanced)
models['XGBoost'] = xgb

# Evaluate models
print("\n📈 Evaluating models...")
print("-" * 60)

for name, model in models.items():
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"\n{name}:")
    print(f"  Accuracy:  {acc:.4f}")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall:    {rec:.4f}")
    print(f"  F1-Score:  {f1:.4f}")
    print(f"  ROC-AUC:   {auc:.4f}")
    
    results.append({
        'Model': name,
        'Accuracy': acc,
        'Precision': prec,
        'Recall': rec,
        'F1-Score': f1,
        'ROC-AUC': auc
    })

# Save results
results_df = pd.DataFrame(results)
print("\n" + "=" * 60)
print("MODEL COMPARISON")
print("=" * 60)
print(results_df.to_string(index=False))

# Find best model
best_idx = results_df['F1-Score'].idxmax()
best_model_name = results_df.loc[best_idx, 'Model']
print(f"\n🏆 Best Model: {best_model_name}")

# Save models
print("\n💾 Saving models...")
MODEL_DIR.mkdir(exist_ok=True)

for name, model in models.items():
    filename = MODEL_DIR / f"{name.lower().replace(' ', '_')}_model.pkl"
    joblib.dump(model, filename)
    print(f"  ✅ {filename.name}")

# Save scaler
scaler_path = MODEL_DIR / 'scaler.pkl'
joblib.dump(scaler, scaler_path)
print(f"  ✅ scaler.pkl")

# Save encoded column names for dashboard
encoded_cols_path = MODEL_DIR / 'encoded_columns.pkl'
joblib.dump(X.columns.tolist(), encoded_cols_path)
print(f"  ✅ encoded_columns.pkl")

# Save a sample row (AFTER encoding) for dashboard to replicate structure
sample_template = X.iloc[0:1].copy()
for col in sample_template.columns:
    sample_template[col] = 0  # Reset values to 0
sample_path = MODEL_DIR / 'input_template.pkl'
joblib.dump(sample_template, sample_path)
print(f"  ✅ input_template.pkl")

# Save feature names (AFTER encoding!)
feature_names_path = MODEL_DIR / 'feature_names.txt'
with open(feature_names_path, 'w') as f:
    f.write('\n'.join(X.columns))  # X after get_dummies
print(f"  ✅ feature_names.txt ({len(X.columns)} features)")

print("\n" + "=" * 60)
print("✅ TRAINING COMPLETE!")
print("=" * 60)
print(f"\nModels saved in: {MODEL_DIR}")
print(f"Best model: {best_model_name}")
print(f"F1-Score: {results_df.loc[best_idx, 'F1-Score']:.4f}")

conn.close()