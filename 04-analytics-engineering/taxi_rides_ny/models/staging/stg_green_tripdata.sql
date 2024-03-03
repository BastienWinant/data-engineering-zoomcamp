with 

source as (

    select * from {{ source('staging', 'green_tripdata') }}

),

renamed as (

    select
        vendor_id,
        lpep_pickup_datetime,
        lpep_dropoff_datetime,
        store_and_fwd_flag,
        ratecode_id,
        pickup_location_id,
        dropoff_location_id,
        passenger_count,
        trip_distance,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        ehail_fee,
        improvement_surcharge,
        total_amount,
        payment_type,
        {{ get_payment_type_description('payment_type') }} as payment_type_described,
        trip_type,
        congestion_surcharge,
        pickup_year,
        pickup_month

    from source

)

select * from renamed
