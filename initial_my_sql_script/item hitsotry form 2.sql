with current_user_swap as (select *,'proposer' as role from swap left join item on swap.item_number_pro = item.item_number
left join user using(email)
where email = 'ebad@gmail.com'
union 
select *, 'conterparty' as role from swap left join item on swap.item_number_counter = item.item_number
left join user using(email)
where email = 'ebad@gmail.com')
select propose_date as 'Proposed Date', swap_status as 'Swap Status',role as 'My Role',
pro.title as 'Proposed Item',con.title as 'Desired Item',
case when current_user_swap.item_number = current_user_swap.item_number_pro then 
(select nickname from user join item using(email) 
where item.item_number = current_user_swap.item_number_counter)
when current_user_swap.item_number = current_user_swap.item_number_counter then
(select nickname from user join item using(email) 
where item.item_number = current_user_swap.item_number_pro)
end as 'Other User' 

from current_user_swap,item con, item pro
where con.item_number = current_user_swap.item_number_counter
and   pro.item_number = current_user_swap.item_number_pro
order by propose_date asc