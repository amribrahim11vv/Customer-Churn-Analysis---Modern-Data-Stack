/*
Staging: Clean and rename columns
*/

with source as (
    select * from {{ ref('Telco_customer_churn') }}
),

cleaned as (
    select
        -- IDs
        "customerID" as customer_id,
        
        -- Location
        "Count" as count_value,
        "Country" as country,
        "State" as state,
        "City" as city,
        "Zip Code" as zip_code,
        "Lat Long" as lat_long,
        "Latitude" as latitude,
        "Longitude" as longitude,
        
        -- Demographics
        "Gender" as gender,
        "Senior Citizen" as is_senior_citizen,
        "Partner" as has_partner,
        "Dependents" as has_dependents,
        
        -- Account
        "Tenure Months" as tenure_months,
        "Contract" as contract_type,
        "Paperless Billing" as has_paperless_billing,
        "Payment Method" as payment_method,
        
        -- Services
        "Phone Service" as has_phone_service,
        "Multiple Lines" as has_multiple_lines,
        "Internet Service" as internet_service_type,
        "Online Security" as has_online_security,
        "Online Backup" as has_online_backup,
        "Device Protection" as has_device_protection,
        "Tech Support" as has_tech_support,
        "Streaming TV" as has_streaming_tv,
        "Streaming Movies" as has_streaming_movies,
        
        -- Financial
        "Monthly Charges" as monthly_charges,
        "Total Charges" as total_charges,
        "CLTV" as customer_lifetime_value,
        
        -- Churn
        "Churn Label" as churn_label,
        "Churn Value" as churn_value,
        "Churn Score" as churn_score,
        "Churn Reason" as churn_reason
        
    from source
)

select * from cleaned