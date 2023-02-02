with mega_temp as 
(	select * from user join item using (email)
	left join accepted_swap on item.item_number = accepted_swap.item_number_pro
    where email = 'rick@gmail.com'
    union
    select * from user join item using (email)
	left join accepted_swap on item.item_number = accepted_swap.item_number_counter
    where email = 'rick@gmail.com')
    select mega_temp.accepted_date as 'Accepted Date', 
    case when mega_temp.item_number = mega_temp.item_number_pro then 'Proposer'
		when mega_temp.item_number = mega_temp.item_number_counter then 'Counter Party'
        end as 'My Role',
        pro.title as 'Proposed Item',con.title as 'Desired Item',
	    case when mega_temp.item_number = mega_temp.item_number_pro then 
        (select nickname from user join item using(email) 
        where item.item_number = mega_temp.item_number_counter)
		when mega_temp.item_number = mega_temp.item_number_counter then
			(select nickname from user join item using(email) 
        where item.item_number = mega_temp.item_number_pro)
        end as 'Other User' 
    
    from mega_temp,item pro, item con
    where pro.item_number=mega_temp.item_number_pro
	and con.item_number = mega_temp.item_number_counter