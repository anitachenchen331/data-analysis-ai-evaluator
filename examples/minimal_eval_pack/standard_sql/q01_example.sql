select
  region,
  count(*) as order_count
from orders
group by region
order by order_count desc;
