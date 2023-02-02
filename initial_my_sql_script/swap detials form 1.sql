with temp_swap_tb as (
select *, case when item_number_pro is null then 'owner' 
else 'proposer' end as myrole 
	from user join item using (email)
	join swap on item.item_number = swap.item_number_pro 
    where email = 'willie@gmail.com'
    union
    select *,case when item_number_pro is null then 'owner' 
else 'counter party' end as myrole  
from user join item using (email)
	join swap on item.item_number = swap.item_number_counter 
    where email = 'willie@gmail.com'
   

)
select temp_swap_tb.item_number_pro, temp_swap_tb.item_number_counter,
propose_date,
case when accepted_date = null then rejected_date 
else accepted_date end as 'Accpeted/Rejected Date',

case when (accepted_date is null and rejected_date is null) then 'Pending'
when  (accepted_date is null and rejected_date is not null) then 'Rejected'
else  'Accepted' end as Status,

case when (myrole = 'proposer') then proposer_rating
else counterparty_rating end as 'Rating Left'
from temp_swap_tb left join accepted_swap using(item_number_pro) left join rejected_swap using(item_number_pro)
where temp_swap_tb.item_number_pro = 5 and temp_swap_tb.item_number_counter = 6