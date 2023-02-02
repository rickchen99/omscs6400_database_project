with current_user_swap as (select *,'proposer' as role from swap left join item on swap.item_number_pro = item.item_number
left join user using(email)
where email = 'rick@gmail.com'
union 
select *, 'conterparty' as role from swap left join item on swap.item_number_counter = item.item_number
left join user using(email)
where email = 'rick@gmail.com')
select role,count(swap_status) as Total,
sum(case when swap_status = 'accepted' then 1 else 0 end) as Accepted, 
sum(case when swap_status = 'rejected' then 1 else 0 end) as Rejected,
round(100*sum(case when swap_status = 'rejected' then 1 else 0 end)/count(*),1) as 'Rejected Rate'

from current_user_swap group by role

