/*
Intermediate: Encode features for ML
*/

with customers as (
    select * from {{ ref('stg_customers') }}
),

features as (
    select
        customer_id,
        
        -- Location (keep original)
        count_value,
        country,
        state,
        city,
        zip_code,
        lat_long,
        latitude,
        longitude,
        
        -- Demographics (encoded: 0/1)
        case when gender = 'Male' then 1 else 0 end as gender_encoded,
        case when is_senior_citizen = 'Yes' then 1 else 0 end as senior_citizen_encoded,
        case when has_partner = 'Yes' then 1 else 0 end as partner_encoded,
        case when has_dependents = 'Yes' then 1 else 0 end as dependents_encoded,
        
        -- Tenure
        tenure_months,
        
        -- Phone services
        case when has_phone_service = 'Yes' then 1 else 0 end as phone_service_encoded,
        case 
            when has_multiple_lines = 'Yes' then 2
            when has_multiple_lines = 'No' then 1
            else 0
        end as multiple_lines_encoded,
        
        -- Internet services (0=no internet, 1=no service, 2=yes)
        case 
            when internet_service_type = 'Fiber optic' then 2
            when internet_service_type = 'DSL' then 1
            else 0
        end as internet_service_encoded,
        
        case 
            when has_online_security = 'Yes' then 2
            when has_online_security = 'No' then 1
            else 0
        end as online_security_encoded,
        
        case 
            when has_online_backup = 'Yes' then 2
            when has_online_backup = 'No' then 1
            else 0
        end as online_backup_encoded,
        
        case 
            when has_device_protection = 'Yes' then 2
            when has_device_protection = 'No' then 1
            else 0
        end as device_protection_encoded,
        
        case 
            when has_tech_support = 'Yes' then 2
            when has_tech_support = 'No' then 1
            else 0
        end as tech_support_encoded,
        
        case 
            when has_streaming_tv = 'Yes' then 2
            when has_streaming_tv = 'No' then 1
            else 0
        end as streaming_tv_encoded,
        
        case 
            when has_streaming_movies = 'Yes' then 2
            when has_streaming_movies = 'No' then 1
            else 0
        end as streaming_movies_encoded,
        
        -- Contract
        case 
            when contract_type = 'Two year' then 2
            when contract_type = 'One year' then 1
            else 0
        end as contract_encoded,
        
        case when has_paperless_billing = 'Yes' then 1 else 0 end as paperless_billing_encoded,
        
        -- Payment method
        case 
            when payment_method like '%Credit card%' then 3
            when payment_method like '%Bank transfer%' then 2
            when payment_method like '%Mailed check%' then 1
            else 0
        end as payment_method_encoded,
        
        -- Financial
        monthly_charges,
        total_charges,
        customer_lifetime_value,
        churn_score,
        
        -- Target
        churn_value as churn
        
    from customers
)

select * from features