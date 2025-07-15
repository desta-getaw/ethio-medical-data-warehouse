with raw as (
  select * from raw.telegram_messages
)
select
  id as message_id,
  message_text,
  channel,
  date::timestamp as message_date,
  jsonb_extract_path_text(other_fields::jsonb, 'views')::int as views
from raw
