with staging as (
  select * from {{ ref('stg_telegram_messages') }}
)
select
  message_id,
  channel,
  message_date,
  length(message_text) as message_length,
  case when message_text ilike '%image%' then true else false end as has_image
from staging
