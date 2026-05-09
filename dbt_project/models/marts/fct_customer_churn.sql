/*
Marts: Final ML-ready dataset
*/

{{ config(materialized='table') }}

with features as (
    select * from {{ ref('int_customer_features') }}
),

final as (
    select
        -- ID (for reference)
        customer_id,
        
        -- Location features
        count_value as "Count",
        country as "Country",
        state as "State", 
        city as "City",
        zip_code as "Zip Code",
        lat_long as "Lat Long",
        latitude as "Latitude",
        longitude as "Longitude",
        
        -- Encoded features (matching training data column names)
        gender_encoded as "Gender",
        senior_citizen_encoded as "Senior Citizen",
        partner_encoded as "Partner",
        dependents_encoded as "Dependents",
        tenure_months as "Tenure Months",
        phone_service_encoded as "Phone Service",
        multiple_lines_encoded as "Multiple Lines",
        internet_service_encoded as "Internet Service",
        online_security_encoded as "Online Security",
        online_backup_encoded as "Online Backup",
        device_protection_encoded as "Device Protection",
        tech_support_encoded as "Tech Support",
        streaming_tv_encoded as "Streaming TV",
        streaming_movies_encoded as "Streaming Movies",
        contract_encoded as "Contract",
        paperless_billing_encoded as "Paperless Billing",
        payment_method_encoded as "Payment Method",
        monthly_charges as "Monthly Charges",
        total_charges as "Total Charges",
        customer_lifetime_value as "CLTV",
        
        -- Target (NO LEAKAGE FEATURES!)
        churn as "Churn Label"
        
    from features
    where customer_id is not null
)

select * from final