            with current_user_swap as (
            select swap.item_number_pro,swap.item_number_counter,swap.propose_date,swap.swap_status,'proposer' as role,
            case when swap_status='accepted' then accepted_date when swap_status='rejected' then rejected_date end as updateDate
            from swap left join item on swap.item_number_pro = item.item_number
            left join accepted_swap on item_number = accepted_swap.item_number_pro left join rejected_swap on item_number=rejected_swap.item_number_pro
            left join user using(email)
            where email = 'usr002@gt.edu' and swap_status != 'pending'
            union 
            select swap.item_number_pro,swap.item_number_counter,swap.propose_date,swap.swap_status, 'counterparty' as role,case when swap_status='accepted' then accepted_date when swap_status='rejected' then rejected_date end as 'Accpet/Reject Date'
            from swap left join item on swap.item_number_counter = item.item_number
            left join accepted_swap on item_number = accepted_swap.item_number_counter left join rejected_swap on item_number=rejected_swap.item_number_counter
            left join user using(email)
            where email = 'usr002@gt.edu' and swap_status != 'pending')
            
            select current_user_swap.item_number_pro, current_user_swap.item_number_counter,propose_date as 'Proposed Date', updateDate as 'Accepted/Rejected Date', swap_status as 'Swap Status',role as 'My Role',
            pro.title as 'Proposed Item',con.title as 'Desired Item',
            case when current_user_swap.role='proposer' then 
            (select nickname from user join item using(email) 
            where item.item_number = current_user_swap.item_number_counter)
            when current_user_swap.role='counterparty' then
            (select nickname from user join item using(email) 
            where item.item_number = current_user_swap.item_number_pro)
            end as 'Other User', 

            case when (current_user_swap.role = 'proposer' and current_user_swap.swap_status = 'accepted')
            then (select counterparty_rating from accepted_swap  where (current_user_swap.item_number_pro = accepted_swap.item_number_pro and current_user_swap.item_number_counter = accepted_swap.item_number_counter ))
            when (current_user_swap.role = 'counterparty' and current_user_swap.swap_status = 'accepted')
            then (select proposer_rating from accepted_swap  where (current_user_swap.item_number_pro = accepted_swap.item_number_pro and current_user_swap.item_number_counter = accepted_swap.item_number_counter ))
            else null end as 'Rating Left'
            from current_user_swap,item con, item pro
            where con.item_number = current_user_swap.item_number_counter
            and   pro.item_number = current_user_swap.item_number_pro 
            order by updateDate desc,propose_date asc