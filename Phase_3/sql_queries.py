def login_form1(email):
    query = "SELECT password FROM user WHERE user.email = '{}';".format(email)
    return query



# Propose Swap Form
def propose_swap_form1(proposed_item,desired_item):
    query = '''
    SELECT desired_item.item_number, proposed_item.item_number, desired_item.item_title , proposed_item.item_title
    FROM swap
    INNER JOIN item proposed_item ON swap.item_number_pro = proposed_item.item_number
    LEFT JOIN item desired_item ON swap.item_number_counter = desired_item.item_number
    WHERE swap.item_number_pro = '{0}' AND swap.item_number_counter = '{1}'
    '''.format(proposed_item,desired_item)
    return query

def propose_swap_form2(proposed_item,desired_item):
    query = '''
    WITH users_cte AS (
    SELECT
    desired.email AS COUNTERPARTY
    ,proposed.email AS PROPOSER
    FROM swap
    LEFT JOIN item desired ON swap.item_number_counter = item.item_number
    LEFT JOIN item proposed ON swap.item_number_pro = item.item_number
    WHERE swap.item_number_pro = '{0}' AND swap.item_number_counter = '{1}'
    )
    , latlong AS ( SELECT users_cte.COUNTERPARTY, users_cte.PROPOSER, counterparty_address.latitude AS counterparty_latitude, counterparty_address.longitude AS counterparty_longitude, proposer_address.latitude AS proposer_latitude, proposer_address.longitude AS proposer_longitude
    FROM users_cte
    LEFT JOIN user counterparty_user ON counterparty_user.email = users_cte.COUNTERPARTY
    LEFT JOIN user proposer_user ON proposer_user.email = users_cte.PROPOSER
    LEFT JOIN address counterparty_address ON counterparty_user.postal_code = counterparty_address.postal_code
    LEFT JOIN address proposer_address ON proposer_user.postal_code = proposer_address.postal_code
    )
    SELECT
    3961 * (2 * ATAN2(SQRT(POW(SIN(RADIANS(counterparty_latitude - proposer_latitude)/2),2) + (COS(RADIANS(counterparty_latitude)) * COS(RADIANS(proposer_latitude)) * POW(SIN(RADIANS(counterparty_longitude - proposer_longitude)/2),2))), SQRT(1-POW(SIN(RADIANS(counterparty_latitude - proposer_latitude)/2),2) + (COS(RADIANS(counterparty_latitude)) * COS(RADIANS(proposer_latitude)) * POW(SIN(RADIANS(counterparty_longitude - proposer_longitude)/2),2))))) AS DISTANCE
    FROM latlong
    '''.format(proposed_item,desired_item)
    return query

def propose_swap_form3(email):
    query = '''
    SELECT item_number, item_type, title ,item_condition FROM item WHERE email = ‘{0}’ 
    ORDER BY item_number
    '''.format(email)
    return query

def propose_swap_form4(proposed_item,desired_item):
    query = '''
    INSERT INTO swap(item_number_pro, item_number_counter, swap_status, propose_date) 
    VALUES ('{0}', '{1}', ‘PENDING’, CURRENT_DATE);
    '''.format(proposed_item,desired_item)
    return query

# Accept/reject swaps form
def accept_reject_swaps_form1(email):
    query = '''
    SELECT swap.propose_date ,swap.item_number_pro ,swap.item_number_counter,user.nickname
    FROM item
    LEFT JOIN swap ON item.item_number = swap.item_number_pro
    LEFT JOIN user ON item.email = user.email
    WHERE email = ‘{0}’
    '''.format(email)
    return query

def accept_reject_swaps_form2(email):
    query = '''
    SELECT
    AVG(accepted_swap.counterparty_rating) AS AVG_COUNTERPARTY_RATING
    FROM item
    LEFT JOIN accepted_swap ON item.item_number = accepted_swap.item_number_pro
    WHERE email = ‘{0}’
    '''.format(email)
    return query

def accept_reject_swaps_form3(proposed_item,desired_item):
    query = '''
    WITH users_cte AS (
    SELECT
    desired.email AS COUNTERPARTY
    ,proposed.email AS PROPOSER
    FROM swap
    LEFT JOIN item desired ON swap.item_number_counter = item.item_number
    LEFT JOIN item proposed ON swap.item_number_pro = item.item_number
    WHERE swap.item_number_pro = '{0}' AND swap.item_number_counter = '{1}'
    )
    , latlong AS ( SELECT users_cte.COUNTERPARTY, users_cte.PROPOSER, counterparty_address.latitude AS counterparty_latitude, counterparty_address.longitude AS counterparty_longitude, proposer_address.latitude AS proposer_latitude, proposer_address.longitude AS proposer_longitude
    FROM users_cte
    LEFT JOIN user counterparty_user ON counterparty_user.email = users_cte.COUNTERPARTY
    LEFT JOIN user proposer_user ON proposer_user.email = users_cte.PROPOSER
    LEFT JOIN address counterparty_address ON counterparty_user.postal_code = counterparty_address.postal_code
    LEFT JOIN address proposer_address ON proposer_user.postal_code = proposer_address.postal_code
    )
    SELECT
    3961 * (2 * ATAN2(SQRT(POW(SIN(RADIANS(counterparty_latitude - proposer_latitude)/2),2) + (COS(RADIANS(counterparty_latitude)) * COS(RADIANS(proposer_latitude)) * POW(SIN(RADIANS(counterparty_longitude - proposer_longitude)/2),2))), SQRT(1-POW(SIN(RADIANS(counterparty_latitude - proposer_latitude)/2),2) + (COS(RADIANS(counterparty_latitude)) * COS(RADIANS(proposer_latitude)) * POW(SIN(RADIANS(counterparty_longitude - proposer_longitude)/2),2))))) AS DISTANCE
    FROM latlong
    '''.format(proposed_item,desired_item)
    return query


def accept_reject_swaps_form5(email):
    query = '''
    SELECT email, first_name FROM user
    WHERE email = ‘{0}’
    '''.format(email)
    return query

def accept_reject_swaps_form6(email):
    query = '''
    SELECT phone_number, is_shared, phone_type FROM phone
    WHERE email = ‘{0}’
    '''.format(email)
    return query

def accept_reject_swaps_form7(proposed_item,desired_item):
    query = '''
    INSERT INTO accepted_swap(item_number_pro,item_number_counter,accepted_date) 
    VALUES ('{0}','{1}',CURRENT_DATE)
    '''.format(proposed_item,desired_item)
    return query

def accept_reject_swaps_form8(proposed_item,desired_item):
    query = '''
    UPDATE swap SET swap_status = ‘accepted’ WHERE item_number_pro = '{0}'
    AND item_number_counter = '{1}'
    '''.format(proposed_item,desired_item)
    return query

def accept_reject_swaps_form9(proposed_item,desired_item):
    query = '''
    INSERT INTO rejected_swap(item_number_pro,item_number_counter,accepted_date) 
    VALUES ('{0}','{1}',CURRENT_DATE)
    '''.format(proposed_item,desired_item)
    return query

def accept_reject_swaps_form10(proposed_item,desired_item):
    query = '''
    UPDATE swap SET swap_status = ‘rejected’ WHERE item_number_pro = '{0}'
    AND item_number_counter = '{1}'
    '''.format(proposed_item,desired_item)
    return query

# Rate Swaps Form
def rate_swaps_form1(email):
    # TODO - Rick please validate this, remove the * selection in the temp table
    query = '''
    WITH temp_tb AS (select *
    FROM user u1 LEFT JOIN item i1 USING(email)
    LEFT JOIN accepted_swap a1 on item_number = a1.item_number_pro
    WHERE email = '{0}' 
    
    UNION

    SELECT *
    FROM user u2 LEFT JOIN item i2 using(email)
    LEFT JOIN accepted_swap a2 on item_number = a2.item_number_counter
    WHERE email = '{0}' )

    SELECT accepted_date,pro.title,con.title
    FROM temp_tb, item pro, item con,user other_user
    WHERE pro.item_number = temp_tb.item_number_pro and con.item_number = temp_tb.item_number_counter
    '''.format(email)
    return query

def rate_swaps_form2(email):
    query = '''
    SELECT nickname FROM user LEFT JOIN item USING(email) WHERE user.email = ‘{0}’
    '''.format(email)
    return query

def rate_swaps_form3(input_proposer_rating,input_counterparty_rating):
    # TODO - Rick please check on this query to make sure it runs
    query = '''
    WITH original_tb AS (select proposer_rating,counterparty_rating FROM accepted_swap)
    UPDATE accepted_swap
    SET proposer_rating = CASE WHEN (counter_party IS NULL then) '{0}'
    else original_tb.propose_rating END,
    counterparty_rating = CASE WHEN(counter_party IS NULL) then '{1}'
    else original_tb.counterparty END
    '''.format(input_proposer_rating,input_counterparty_rating)
    return query

# Swap History Form
def swap_history_form1(email):
    query_proposer = '''
    SELECT
    SUM(CASE WHEN swap.propose_date IS NOT NULL THEN 1 ELSE 0 END) AS SWAP_COUNT,
    SUM(CASE WHEN accepted_swap.accepted_date IS NOT NULL THEN 1 ELSE 0 END) AS ACCEPTED_COUNT,
    SUM(CASE WHEN rejected_swap.rejected_Date IS NOT NULL THEN 1 ELSE 0 END) AS REJECTED_COUNT,
    SUM(CASE WHEN rejected_swap.rejected_Date IS NOT NULL THEN 1 ELSE 0 END) /SUM(CASE WHEN swap.propose_date IS NOT NULL THEN 1 ELSE 0 END) AS REJECTED_PCT
    FROM item
    INNER JOIN swap ON item.item_number = swap.item_number_pro
    LEFT JOIN accepted_swap ON swap.item_number_pro = accepted_swap.item_number_pro AND swap.item_number_counter = accepted_swap.item_number_counter
    LEFT JOIN rejected_swap ON swap.item_number_pro = rejected_swap.item_number_pro AND swap.item_number_counter = rejected_swap.item_number_counter
    WHERE item.email = '{0}'
    '''.format(email)

    query_counterparty = '''
    SELECT
    SUM(CASE WHEN swap.propose_date IS NOT NULL THEN 1 ELSE 0 END) AS SWAP_COUNT,
    SUM(CASE WHEN accepted_swap.accepted_date IS NOT NULL THEN 1 ELSE 0 END) AS ACCEPTED_COUNT,
    SUM(CASE WHEN rejected_swap.rejected_Date IS NOT NULL THEN 1 ELSE 0 END) AS REJECTED_COUNT,
    SUM(CASE WHEN rejected_swap.rejected_Date IS NOT NULL THEN 1 ELSE 0 END) /SUM(CASE WHEN swap.propose_date IS NOT NULL THEN 1 ELSE 0 END) AS REJECTED_PCT
    FROM item
    INNER JOIN swap ON item.item_number = swap.item_number_counter
    LEFT JOIN accepted_swap on swap.item_number_pro = accepted_swap.item_number_pro AND swap.item_number_counter = accepted_swap.item_number_counter
    LEFT JOIN rejected_swap ON swap.item_number_pro = rejected_swap.item_number_pro AND swap.item_number_counter = rejected_swap.item_number_counter
    WHERE item.email = ‘{0}’
    '''.format(email)
    return (query_proposer,query_counterparty)

def swap_history_form2(email):
    query = '''
    SELECT proposed_swap.propose_date ,accepted_swap.accepted_date , rejected_swap.rejected_date ,‘Proposer’ AS user_role , item.title , desired.title, other_user.nickname, accepted_swap.counterparty_rating
    FROM item
    LEFT JOIN swap proposed_swap ON item.item_number = proposed_swap.item_number_pro
    LEFT JOIN accepted_swap 
    ON proposed_swap.item_number_pro = accepted_swap.item_number_pro
    AND  proposed_swap.item_number_counter = accepted_swap.item_number_counter
    LEFT JOIN rejected_swap 
    ON proposed_swap.item_number_pro = rejected_swap.item_number_pro
    AND  proposed_swap.item_number_counter = rejected_swap.item_number_counter
    LEFT JOIN item desired ON proposed_swap.item_number_counter = desired.item_number
    LEFT JOIN user other_user ON desired.email = other_user.email
    WHERE item.email = ‘{0}’

    UNION ALL

    SELECT proposed_swap.propose_date ,accepted_swap.accepted_date, rejected_swap.rejected_date, ‘Proposer’ AS user_role , item.title ,desired.title, other_user.nickname, accepted_swap.counterparty_rating
    FROM item
    LEFT JOIN swap proposed_swap ON item.item_number = proposed_swap.item_number_pro
    LEFT JOIN accepted_swap 
    ON proposed_swap.item_number_pro = accepted_swap.item_number_pro
    AND  proposed_swap.item_number_counter = accepted_swap.item_number_counter
    LEFT JOIN rejected_swap 
    ON proposed_swap.item_number_pro = rejected_swap.item_number_pro
    AND  proposed_swap.item_number_counter = rejected_swap.item_number_counter
    LEFT JOIN item desired ON proposed_swap.item_number_counter = desired.item_number
    LEFT JOIN user other_user ON desired.email = other_user.email
    WHERE item.email = ‘{0}’
    '''.format(email)
    return query

# Swap Details Form
def swap_details_form1(proposed_item,desired_item):
    # TODO - this is the best distance query, chris to propogate this across other queries
    query = '''
    WITH users_cte AS (
    SELECT desired.email AS COUNTERPARTY, proposed.email AS PROPOSER
    FROM swap
    LEFT JOIN item desired ON swap.item_number_counter = desired.item_number
    LEFT JOIN item proposed ON swap.item_number_pro = proposed.item_number
    WHERE swap.item_number_pro = '{0}'
    AND  swap.item_number_counter = '{1}'
    )
    , latlong AS (
    SELECT users_cte.COUNTERPARTY, users_cte.PROPOSER, counterparty_address.latitude AS counterparty_latitude, counterparty_address.longitude AS counterparty_longitude, proposer_address.latitude AS proposer_latitude, proposer_address.longitude AS proposer_longitude

    FROM users_cte
    LEFT JOIN user counterparty_user ON counterparty_user.email = users_cte.COUNTERPARTY
    LEFT JOIN user proposer_user ON proposer_user.email = users_cte.PROPOSER
    LEFT JOIN address counterparty_address ON counterparty_user.postal_code = counterparty_address.postal_code
    LEFT JOIN address proposer_address ON proposer_user.postal_code = proposer_address.postal_code
    )
    ,distance AS (
    SELECT
    3961 * (2 * ATAN2(SQRT(POW(SIN(RADIANS(counterparty_latitude - proposer_latitude)/2),2) + (COS(RADIANS(counterparty_latitude)) * COS(RADIANS(proposer_latitude)) * POW(SIN(RADIANS(counterparty_longitude - proposer_longitude)/2),2))), SQRT(1-POW(SIN(RADIANS(counterparty_latitude - proposer_latitude)/2),2) + (COS(RADIANS(counterparty_latitude)) * COS(RADIANS(proposer_latitude)) * POW(SIN(RADIANS(counterparty_longitude - proposer_longitude)/2),2)))))
    AS DISTANCE
    FROM latlong
    )
    SELECT item.email, item.title, item.item_description, swap.swap_status , swap.propose_date, accepted_swap.accepted_date, accepted_swap.proposer_rating, accepted_swap.counterparty_rating, distance.distance
    FROM swap 
    INNER JOIN item ON item.item_number = swap.item_number_pro
    LEFT JOIN accepted_swap ON swap.item_number_pro = accepted_swap.item_number_pro AND swap.item_number_counter = accepted_swap.item_number_counter
    LEFT JOIN distance ON 1=1
    WHERE swap.item_number_pro = '{0}'
    AND  swap.item_number_counter = '{1}'
    '''.format(proposed_item,desired_item)
    return query

def swap_details_form2(input_counterparty_rating):
    # Rick - please add inputs so we can find the appropriate swap to insert into here
    query = '''
    WITH original_tb AS (select proposer_rating,counterparty_rating FROM accepted_swap)
    UPDATE accepted_swap
    SET counterparty_rating = CASE WHEN counterparty_rating IS NULL then '{0}'
    else original_tb.counterparty END
    '''.format(input_counterparty_rating)
    return query
