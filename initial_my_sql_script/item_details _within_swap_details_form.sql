
select i.item_number as 'Item #' ,i.title as Title,i.item_condition as 'Condition',i.item_description as Description,
(case  when exists(select * from board_game where item_number = i.item_number) then 'Board Game'
 when exists(select * from computer_game where item_number = i.item_number) then 'Computer Game'
 when exists(select * from video_game where item_number = i.item_number) then 'Video Game'
 when exists(select * from card_game where item_number = i.item_number) then 'Card Game'
 when exists(select * from jigsaw where item_number = i.item_number) then 'Jigsaw'
else null 
end) as 'Game Type' ,video_game.platform_type AS Platform, 
video_game.media AS Media,  jigsaw.piece_count AS 'Number of pieces', computer_game.os AS 'OS'
from item i LEFT JOIN video_game USING (item_number) LEFT JOIN computer_game USING (item_number)
LEFT JOIN card_game USING (item_number) LEFT JOIN board_game USING (item_number)
LEFT JOIN jigsaw USING (item_number) where item_number = 1

delete from swap where item_number_pro =15 and item_number_counter=10
select * from item left join user using(email) where item_number = 24
select * from user

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
            end as 'Other User' ,
            
            case when (current_user_swap.role = 'proposer' and current_user_swap.swap_status != 'rejected')
            then (select proposer_rating from accepted_swap join swap on accepted_swap.item_number_counter = swap.item_number_counter and accepted_swap.item_number_pro = swap.item_number_pro)
			case when current_user_swap.role = 'counterparty' and current_user_swap.swap_status is not 'rejected'
            then (select proposer_rating from accepted_swap join swap on accepted_swap.item_number_counter = swap.item_number_counter and accepted_swap.item_number_pro = swap.item_number_pro)
            else null end as 'Rating Left'

            from current_user_swap,item con, item pro
            where con.item_number = current_user_swap.item_number_counter
            and   pro.item_number = current_user_swap.item_number_pro
            
            order by propose_date asc
            select count(*) from user
            select count(*) from address
            set 
            truncate table swap
            SET FOREIGN_KEY_CHECKS = 0 
            select count(*) from phoneis_sharedphone_user_email
            
                    
        SELECT Table_1.item_number AS 'Item #', game_types.item_type AS 'Game type', Table_1.title AS Title, 
        Table_1.item_condition AS 'Condition', Table_1.item_description AS Description, 0 AS 'Distance'
        FROM
        (
        SELECT i.item_number,  i.title, i.item_condition, i.item_description FROM item i
        LEFT JOIN user ON i.email = user.email
        LEFT JOIN swap s ON i.item_number = s.item_number_counter OR i.item_number = s.item_number_pro
        WHERE (s.swap_status IS NULL or s.swap_status LIKE "rejected") 
        AND user.postal_code = (SELECT postal_code FROM user WHERE user.email = 'usr002@gt.edu') AND 
        user.email = 'usr002@gt.edu' ORDER BY item_number ASC
        ) As Table_1
        LEFT JOIN ( SELECT item_number, 'computer_game' AS item_type
        FROM computer_game UNION SELECT item_number, 'video_game' AS item_type
        FROM video_game UNION SELECT item_number, 'card_game' AS item_type
        FROM card_game UNION
        SELECT item_number, 'board_game' AS item_type FROM board_game
        UNION SELECT item_number, 'jigsaw' AS item_type
        FROM jigsaw) AS game_types USING (item_number);
        
        select * from item where email = 'usr002@gt.edu'
        
        select * from user where postal_code = (select postal_code from user where email = 'usr003@gt.edu')
        
        select count(*) from rejected_swap
        set
        select * from user where email ='usr859@gt.edu'
        
        select * from accepted_swap where item_number_pro = 1011 and item_number_counter = 4
        
        select * from accepted_swap where proposer_rating is null
        select * from item,accepted_swap where email = 'usr002@gt.edu' and item_number in(item_number_pro,item_number_counter)
        select * from phone where email = 'ebad@gmail.com'
		select * from item where item_number =19
			
        select * from item left join swap on (item_number = item_number_pro or item_number = item_number_counter) where email = 'usr002@gt.edu' and swap_status is null
        item_description
        SELECT * FROM user
		LEFT JOIN item ON item.email = user.email
		LEFT JOIN swap ON swap.item_number_counter = item.item_number
		WHERE user.email = 'usr002@gt.edu' AND swap_status = 'pending' AND CURDATE() - propose_date > 5;
		update accepted_swap set proposer_rating = null,counterparty_rating =null where item_number_pro = 15 and item_number_counter=5335
        update item set item_description ='longgggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaagggggggggggggggggggggggggggggggggggggggggggggggggggggg'  
        where item_number = 1018