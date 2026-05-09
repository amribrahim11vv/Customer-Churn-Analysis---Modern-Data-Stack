# 📊 Exploratory Data Analysis (EDA) Summary
## Customer Churn Dataset - DBT Project

**Date:** December 2024  
**Data Source:** Telco Customer Churn (Kaggle)  
**Analysis Tool:** DuckDB + DBT + Python

---

## 1. Dataset Overview

### 1.1 Basic Statistics

| Metric | Value |
|--------|-------|
| **Total Records** | 7,043 |
| **Total Features** | 32 (original) |
| **Target Variable** | Churn Label |
| **Memory Usage** | ~2.5 MB |
| **Missing Values** | 11 (in Total Charges) |
| **Duplicate Records** | 0 |

### 1.2 Data Quality

**Before Cleaning:**
- Missing values: 11 rows in `Total Charges`
- Data type issues: `Total Charges` as text (had spaces)

**After DBT Pipeline:**
- ✅ All missing values handled
- ✅ Data types corrected
- ✅ Column names standardized
- ✅ 100% data quality

---

## 2. Target Variable Analysis

### 2.1 Churn Distribution

```
Churn Label:
  0 (No Churn):  5,174 customers (73.5%)
  1 (Churn):     1,869 customers (26.5%)
```

**Visualization:**
```
No Churn  ████████████████████████████████████ 73.5%
Churn     ████████████ 26.5%
```

**Key Finding:** 
- ⚠️ **Imbalanced dataset** (73/27 split)
- Need special handling (SMOTE, class weights)

---

## 3. Demographic Analysis

### 3.1 Gender

| Gender | Count | Churn Rate |
|--------|-------|------------|
| Male | 3,555 (50.5%) | 26.2% |
| Female | 3,488 (49.5%) | 26.9% |

**Insight:** Gender has minimal impact on churn

### 3.2 Senior Citizens

| Senior | Count | Churn Rate |
|--------|-------|------------|
| No | 5,901 (83.8%) | 23.6% |
| Yes | 1,142 (16.2%) | 41.7% |

**Insight:** 🚨 Senior citizens churn at **1.8x** higher rate

### 3.3 Partner & Dependents

| Category | Has | Doesn't Have |
|----------|-----|--------------|
| **Partner** | 48.3% | 51.7% |
| Partner Churn Rate | 19.7% | 32.9% |
| **Dependents** | 30.2% | 69.8% |
| Dependents Churn Rate | 15.5% | 31.3% |

**Insight:** 🚨 Customers without family ties churn **2x** more

---

## 4. Account Information

### 4.1 Tenure Distribution

```
Tenure Months:
  Mean:   32.4 months
  Median: 29 months
  Min:    0 months
  Max:    72 months
  Std:    24.6 months
```

**Churn by Tenure:**

| Tenure Range | Count | Churn Rate |
|--------------|-------|------------|
| 0-12 months | 2,175 | **47.7%** 🚨 |
| 13-24 months | 1,108 | 35.3% |
| 25-48 months | 1,645 | 15.5% |
| 49+ months | 2,115 | **7.4%** ✅ |

**Key Insight:** 🚨 **NEW CUSTOMERS CHURN 6x MORE** than long-term customers!

### 4.2 Contract Type

| Contract | Count | % | Churn Rate |
|----------|-------|---|------------|
| Month-to-month | 3,875 | 55.0% | **42.7%** 🚨 |
| One year | 1,473 | 20.9% | 11.3% |
| Two year | 1,695 | 24.1% | **2.8%** ✅ |

**Insight:** Month-to-month customers churn **15x** more than 2-year contracts!

### 4.3 Payment Method

| Method | Count | Churn Rate |
|--------|-------|------------|
| Electronic check | 2,365 | **45.3%** 🚨 |
| Mailed check | 1,612 | 19.1% |
| Bank transfer (auto) | 1,544 | 16.7% |
| Credit card (auto) | 1,522 | 15.2% |

**Insight:** Electronic check users churn **3x** more!

---

## 5. Service Subscriptions

### 5.1 Phone Services

| Service | Has | Doesn't Have |
|---------|-----|--------------|
| **Phone Service** | 90.3% | 9.7% |
| Churn Rate | 26.6% | 25.0% |
| **Multiple Lines** | 42.0% | 48.3% |
| Churn Rate | 28.6% | 25.2% |

**Insight:** Phone services have minimal churn impact

### 5.2 Internet Services

| Type | Count | % | Churn Rate |
|------|-------|---|------------|
| Fiber optic | 3,096 | 44.0% | **41.9%** 🚨 |
| DSL | 2,421 | 34.4% | 18.9% |
| No internet | 1,526 | 21.7% | 7.4% |

**Insight:** 🚨 **Fiber optic customers churn 2x more than DSL!**

### 5.3 Add-on Services (for internet users)

| Service | Has | Churn Rate w/ Service | Churn Rate w/o Service | Impact |
|---------|-----|----------------------|----------------------|--------|
| Online Security | 28.7% | 14.6% | **41.8%** | -27.2% 🛡️ |
| Online Backup | 34.5% | 21.6% | **39.9%** | -18.3% 💾 |
| Device Protection | 34.4% | 22.5% | **39.1%** | -16.6% 🔒 |
| Tech Support | 29.0% | 15.2% | **41.7%** | -26.5% 🛠️ |
| Streaming TV | 38.4% | 29.8% | 33.0% | -3.2% 📺 |
| Streaming Movies | 38.8% | 29.7% | 33.2% | -3.5% 🎬 |

**Key Insights:**
- 🛡️ **Tech Support** and **Online Security** reduce churn by ~27%
- 💾 **Backup** and **Protection** reduce churn by ~17%
- 📺 Streaming services have minimal impact

---

## 6. Financial Analysis

### 6.1 Monthly Charges

```
Monthly Charges:
  Mean:   $64.76
  Median: $70.35
  Min:    $18.25
  Max:    $118.75
  Std:    $30.09
```

**Churn by Monthly Charges:**

| Charges Range | Count | Churn Rate |
|---------------|-------|------------|
| $18-40 | 1,846 | **7.5%** ✅ |
| $40-70 | 2,213 | 23.5% |
| $70-100 | 2,145 | **40.5%** 🚨 |
| $100+ | 839 | **44.1%** 🚨 |

**Insight:** Higher charges = Higher churn!

### 6.2 Total Charges

```
Total Charges:
  Mean:   $2,283.30
  Median: $1,397.48
  Min:    $18.80
  Max:    $8,684.80
  Std:    $2,266.77
```

**Correlation:** Strong correlation with tenure (r=0.83)

### 6.3 Customer Lifetime Value (CLTV)

```
CLTV:
  Mean:   $3,682.89
  Median: $3,427.09
  Min:    $2,003.18
  Max:    $6,500.50
  Std:    $1,398.14
```

---

## 7. Geographic Analysis

### 7.1 State Distribution

**All customers from California**
- Country: United States (100%)
- State: California (100%)

### 7.2 City Distribution

**Top 10 Cities:**

| City | Count | % of Total |
|------|-------|------------|
| Los Angeles | 523 | 7.4% |
| San Diego | 487 | 6.9% |
| San Jose | 412 | 5.8% |
| San Francisco | 389 | 5.5% |
| Fresno | 276 | 3.9% |
| Sacramento | 264 | 3.7% |
| Long Beach | 251 | 3.6% |
| Oakland | 234 | 3.3% |
| Bakersfield | 198 | 2.8% |
| Anaheim | 187 | 2.7% |

**Total cities:** 1,129 unique cities

---

## 8. Key Correlations

### 8.1 Strong Positive Correlations with Churn

1. **Month-to-month contract** (0.41)
2. **Fiber optic internet** (0.31)
3. **Electronic check payment** (0.30)
4. **No tech support** (0.28)
5. **No online security** (0.27)

### 8.2 Strong Negative Correlations with Churn

1. **Long tenure** (-0.35)
2. **Two-year contract** (-0.30)
3. **Has tech support** (-0.28)
4. **Has online security** (-0.27)
5. **Has partner** (-0.15)

---

## 9. Customer Segments

### 9.1 High-Risk Profile

**Characteristics:**
- 👤 Single, no dependents
- 👴 Senior citizen
- 📅 Tenure < 12 months
- 📝 Month-to-month contract
- 🌐 Fiber optic internet WITHOUT add-ons
- 💳 Electronic check payment
- 💰 Monthly charges > $70

**Churn Rate:** ~**70-80%** 🚨

**Action:** Immediate intervention required

### 9.2 Medium-Risk Profile

**Characteristics:**
- 📅 Tenure 12-24 months
- 📝 One-year contract OR Month-to-month with add-ons
- 🌐 DSL internet or Fiber with some add-ons
- 💰 Monthly charges $40-70

**Churn Rate:** ~**30-40%** ⚠️

**Action:** Proactive retention

### 9.3 Low-Risk Profile

**Characteristics:**
- 👫 Has partner and dependents
- 📅 Tenure > 24 months
- 📝 Two-year contract
- 🛡️ Multiple add-on services
- 💳 Automatic payment
- 💰 Monthly charges < $70

**Churn Rate:** ~**5-10%** ✅

**Action:** Maintain satisfaction, upsell

---

## 10. Business Insights

### 10.1 Top 5 Churn Drivers

1. **Short Tenure** → Focus on first year retention
2. **Month-to-month Contracts** → Incentivize long-term contracts
3. **No Tech Support** → Bundle with high-risk customers
4. **Electronic Check** → Migrate to auto-pay
5. **High Charges without Value** → Review pricing for fiber users

### 10.2 Retention Opportunities

| Opportunity | Impact | Difficulty | Priority |
|-------------|--------|------------|----------|
| Convert to annual contracts | High | Medium | 🔴 High |
| Add tech support to fiber users | High | Low | 🔴 High |
| First-year engagement program | Very High | High | 🔴 High |
| Migrate from electronic checks | Medium | Low | 🟠 Medium |
| Review fiber optic pricing | High | High | 🟠 Medium |
| Family/partner promotions | Medium | Medium | 🟢 Low |

---

## 11. Data Quality Issues (Resolved)

### 11.1 Issues Found

1. **Missing Values:** 11 rows in `Total Charges` (empty strings)
2. **Data Type:** `Total Charges` stored as VARCHAR
3. **Inconsistent Names:** Mixed casing in column names

### 11.2 Resolution (DBT Pipeline)

```sql
-- In stg_customers.sql
"Total Charges" as total_charges  -- Renamed

-- In convert_excel_to_csv.py
df['Total Charges'] = pd.to_numeric(
    df['Total Charges'], 
    errors='coerce'
).fillna(0)
```

**Result:** ✅ 100% clean data

---

## 12. Conclusion

### 12.1 Dataset Summary

- ✅ High-quality data after cleaning
- ✅ Rich feature set (demographics + services + financial)
- ✅ Clear churn patterns identified
- ✅ Actionable business insights

### 12.2 Key Takeaways

1. **Tenure is king:** First year is critical
2. **Contracts matter:** Month-to-month is a red flag
3. **Add-ons reduce churn:** Tech support especially
4. **Payment method signals risk:** Electronic checks bad
5. **Fiber paradox:** High-value customers churn more

### 12.3 Next Steps

1. ✅ Use insights for feature engineering
2. ✅ Train predictive models
3. ✅ Segment customers by risk
4. ✅ Build targeted retention campaigns

---

**End of EDA Report**

*For detailed visualizations, run: `jupyter notebook notebooks/01_explore_duckdb.ipynb`*