class UserRegistrationForm:

    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db

    def register_user(self, email, nickname, password, first_name, last_name, postal_code):
        self.cursor.execute(
            "INSERT INTO user (email, password, nickname, first_name, last_name, postal_code) VALUES (%s, %s, %s, %s, %s, %s)",
            (email, password, nickname, first_name, last_name, postal_code),
            )
        self.db.commit()

    def register_phone_number(self, phone_number, email, phone_type, share_phone_number):
        self.cursor.execute(
            "INSERT INTO phone (phone_number, email, phone_type, is_shared) VALUES (%s, %s, %s, %s)",
            (phone_number, email, phone_type, share_phone_number),
            )
        self.db.commit()


class LoginForm:

    def __init__(self, cursor):
        self.cursor = cursor

    def email_login_attempt(self, login_attempt):
        query_email = "SELECT email, password FROM user WHERE email = %(login_attempt)s"
        self.cursor.execute(query_email, { 'login_attempt': login_attempt})
        return self.cursor.fetchall()[0]

    def phone_login_attempt(self, login_attempt):
        query_phone = "SELECT user.email, user.password, phone.phone_number \
        FROM phone LEFT JOIN user on user.email = phone.email \
        WHERE phone.phone_number = %(login_attempt)s"
        self.cursor.execute(query_phone, { 'login_attempt': login_attempt})
        return self.cursor.fetchall()[0]

class MainMenuForm:

    def __init__(self, cursor):
        self.cursor = cursor


    def welcome_message(self, session):
        query_welcome = "SELECT first_name, last_name FROM user WHERE email = %(session)s"
        self.cursor.execute(query_welcome, { 'session': session})
        return self.cursor.fetchall()[0]

    def display_my_rating(self, session):
        query_my_rating = " SELECT (SUM(proposer_rating) + SUM(counterparty_rating)) / \
        (COUNT(proposer_rating) + COUNT(counterparty_rating)) AS total_rating \
        FROM accepted_swap AS acc \
        LEFT JOIN swap AS a ON acc.item_number_pro = a.item_number_pro \
        LEFT JOIN item AS b ON b.item_number = a.item_number_pro \
        LEFT JOIN user AS p ON p.email = b.email \
        LEFT JOIN swap AS c ON acc.item_number_counter = c.item_number_counter \
        LEFT JOIN item AS d ON d.item_number = c.item_number_counter \
        LEFT JOIN user AS w ON w.email = d.email \
        WHERE p.email = %(session)s OR w.email = %(session)s"
        self.cursor.execute(query_my_rating, { 'session': session})
        return self.cursor.fetchall()[0]

    def display_unaccepted_swaps(self, session):
        query_unaccepted_swaps = "SELECT COUNT(swap_status) FROM user \
        LEFT JOIN item ON item.email = user.email \
        LEFT JOIN swap ON swap.item_number_counter = item.item_number \
        WHERE user.email = %(session)s AND swap_status = 'pending'"
        self.cursor.execute(query_unaccepted_swaps, { 'session': session})
        return self.cursor.fetchall()[0]

    def unaccepted_swaps_over_five_days (self, session):
        query_five_days = "SELECT COUNT(swap_status) FROM user \
        LEFT JOIN item ON item.email = user.email \
        LEFT JOIN swap ON swap.item_number_counter = item.item_number \
        WHERE user.email = %(session)s AND swap_status = 'pending' AND CURDATE() - propose_date > 5;"
        self.cursor.execute(query_five_days, { 'session': session})
        return self.cursor.fetchall()[0]

    def display_unrated_swaps(self, session):
        query_unrated_swaps = "SELECT COUNT(*) AS Unrated_Swaps \
        FROM accepted_swap AS acc \
        LEFT JOIN swap AS a ON acc.item_number_pro = a.item_number_pro \
        LEFT JOIN item AS b ON b.item_number = a.item_number_pro \
        LEFT JOIN user AS p ON p.email = b.email \
        LEFT JOIN swap AS c ON acc.item_number_counter = c.item_number_counter \
        LEFT JOIN item AS d ON d.item_number = c.item_number_counter \
        LEFT JOIN user AS w ON w.email = d.email \
        WHERE (proposer_rating IS NULL AND w.email = %(session)s) OR (counterparty_rating IS NULL AND p.email = %(session)s);"
        self.cursor.execute(query_unrated_swaps, { 'session': session})
        return self.cursor.fetchall()[0]


    # TODO - not sure the count of unrated swaps is right

class UpdateUserInfoForm:

    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db

    def allow_update_access_swaps(self, session):
        query_any_unaccepted_swaps = "SELECT COUNT(*) \
        FROM User AS u \
        LEFT JOIN item as i ON i.email = u.email \
        LEFT JOIN swap AS a ON a.item_number_counter = i.item_number \
        LEFT JOIN swap as b ON b.item_number_pro = i.item_number \
        WHERE u.email = %(session)s AND (a.swap_status = 'pending' OR b.swap_status = 'pending');"
        self.cursor.execute(query_any_unaccepted_swaps, { 'session': session})
        return self.cursor.fetchall()[0]

    def allow_update_access_rating(self, session):
        query_unrated_swaps = "SELECT COUNT(*) AS Unrated_Swaps \
        FROM accepted_swap AS acc \
        LEFT JOIN swap AS a ON acc.item_number_pro = a.item_number_pro \
        LEFT JOIN item AS b ON b.item_number = a.item_number_pro \
        LEFT JOIN user AS p ON p.email = b.email \
        LEFT JOIN swap AS c ON acc.item_number_counter = c.item_number_counter \
        LEFT JOIN item AS d ON d.item_number = c.item_number_counter \
        LEFT JOIN user AS w ON w.email = d.email \
        WHERE (proposer_rating IS NULL AND w.email = %(session)s) OR (counterparty_rating IS NULL AND p.email = %(session)s);"
        self.cursor.execute(query_unrated_swaps, { 'session': session})
        return self.cursor.fetchall()[0]

    def display_my_info(self, session):
        query_my_info = "SELECT u.email, password, nickname, first_name, last_name, u.postal_code, \
        p.phone_number, p.phone_type, p.is_shared, a.city, a.state \
        FROM user as u \
        LEFT JOIN phone as p ON u.email = p.email \
        LEFT JOIN address as a ON u.postal_code = a.postal_code \
        WHERE u.email = %(session)s"
        self.cursor.execute(query_my_info, { 'session': session})
        return self.cursor.fetchall()[0]

    def update_password(self, password, session):
        update_my_password = (
            "UPDATE user SET password = %s "
            "WHERE email = %s ")
        self.cursor.execute(update_my_password, (password, session))		
        self.db.commit()

    def update_first_name(self, first_name, session):
        update_my_first_name = (
            "UPDATE user SET first_name = %s "
            "WHERE email = %s ")
        self.cursor.execute(update_my_first_name, (first_name, session))		
        self.db.commit()

    def update_last_name(self, last_name, session):
        update_my_last_name = (
            "UPDATE user SET last_name = %s "
            "WHERE email = %s ")
        self.cursor.execute(update_my_last_name, (last_name, session))		
        self.db.commit()

    def update_nickname(self, nickname, session):
        update_my_nickname = (
            "UPDATE user SET nickname = %s "
            "WHERE email = %s ")
        self.cursor.execute(update_my_nickname, (nickname, session))		
        self.db.commit()

    def update_postal_code(self, postal_code, session):
        update_my_postal_code = (
            "UPDATE user SET postal_code = %s "
            "WHERE email = %s ")
        self.cursor.execute(update_my_postal_code, (postal_code, session))		
        self.db.commit()

    def update_phone_number(self, phone_number, session):
        update_my_phone_number = (
            "UPDATE phone SET phone_number = %s "
            "WHERE email = %s ")
        self.cursor.execute(update_my_phone_number, (phone_number, session))		
        self.db.commit()

    def update_phone_type(self, phone_type, session):
        update_my_phone_type = (
            "UPDATE phone SET phone_type = %s "
            "WHERE email = %s ")
        self.cursor.execute(update_my_phone_type, (phone_type, session))		
        self.db.commit()

    def update_is_shared(self, is_shared, session):
        update_is_shared_choice = (
            "UPDATE phone SET is_shared = %s "
            "WHERE email = %s ")
        self.cursor.execute(update_is_shared_choice, (is_shared, session))		
        self.db.commit()

class RateSwapForm:

    def __init__(self, cursor):
        self.cursor = cursor

    def display_table(self,session):
        query = '''
        WITH temp_tb AS (
        select a1.accepted_date
        , 'Proposer' as my_role
        , i1.item_number
        , i1.title as proposed_item
        , other_item.title as desired_item
        , CONCAT(user2.first_name,' ',user2.last_name) as other_user
        , a1.item_number_pro as proposed
        , a1.item_number_counter as desired
        FROM item i1
        INNER JOIN accepted_swap a1 on i1.item_number = a1.item_number_pro
        LEFT JOIN item other_item on a1.item_number_counter = other_item.item_number
        LEFT JOIN user user2 on other_item.email = user2.email
        WHERE i1.email = '{0}' AND proposer_rating is null
        
        UNION

        SELECT a2.accepted_date
        ,'Counterparty' as my_role
        , i2.item_number
        , other_item.title as proposed_item
        , i2.title as desired_item
        , CONCAT(user2.first_name,' ',user2.last_name) as other_user
        , a2.item_number_pro as proposed
        , a2.item_number_counter as desired
        FROM item i2
        INNER JOIN accepted_swap a2 on item_number = a2.item_number_counter
        LEFT JOIN item other_item on a2.item_number_pro = other_item.item_number
        LEFT JOIN user user2 on other_item.email = user2.email
        WHERE i2.email = '{0}' AND counterparty_rating IS NULL)

        SELECT *
        from temp_tb 
        ORDER BY accepted_date desc
        '''.format(session)
        self.cursor.execute(query, { 'session': session})
        return self.cursor.fetchall()
    
    def update_rating(self,rating,role,proposed,desired):
        query= '''
        UPDATE accepted_swap
        SET proposer_rating = CASE WHEN '{1}' = 'Proposer' THEN {0} ELSE proposer_rating END
        ,counterparty_rating = CASE WHEN '{1}' = 'Counterparty' THEN {0} ELSE counterparty_rating END
        WHERE item_number_pro = {2} AND item_number_counter = {3}
        '''.format(rating,role,proposed,desired)
        print(query)
        self.cursor.execute(query)

    # def rate_swaps_form2(self,email):
    # 	query = '''
    # 	SELECT nickname FROM user INNER JOIN item USING(email) WHERE user.email = ‘{0}’
    # 	'''.format(email)
    # 	return query

    # def rate_swaps_form3(self,input_proposer_rating,input_counterparty_rating):
    # 	# TODO - Rick please check on this query to make sure it runs
    # 	query = '''
    # 	WITH original_tb AS (select proposer_rating,counterparty_rating FROM accepted_swap)
    # 	UPDATE accepted_swap
    # 	SET proposer_rating = CASE WHEN (counter_party IS NULL then) '{0}'
    # 	else original_tb.propose_rating END,
    # 	counterparty_rating = CASE WHEN(counter_party IS NULL) then '{1}'
    # 	else original_tb.counterparty END
    # 	'''.format(input_proposer_rating,input_counterparty_rating)
    # 	return query

class AcceptRejectForm:

    def __init__(self, cursor):
        self.cursor = cursor
    
    def fetch_swaps(self,session):
        query = '''
        SELECT swap.propose_date ,swap.item_number_pro,item.title as pro_title,swap.item_number_counter,other_item.title as counter_title,user.nickname,other_item.email as other_user1,other_user.nickname as other_user_name
        FROM item
        INNER JOIN swap ON item.item_number = swap.item_number_counter
        LEFT JOIN user ON item.email = user.email
        LEFT JOIN item other_item ON other_item.item_number = swap.item_number_pro
        LEFT JOIN user other_user ON other_item.email = user.email
        WHERE item.email = "{0}" AND LOWER(swap.swap_status) = "pending"
        '''.format(session)
        
        print(query)

        self.cursor.execute(query, { 'session': session})
        base_table = self.cursor.fetchall()
        base_table = list(list(x) for x in base_table)
        print(base_table)
        
        i = 0
        for row in base_table:
            print('ROW: ', row)
            other_user = row[6]
            item_number_pro = row[1]
            item_number_counter = row[3]

            rating = '''
            SELECT
            COALESCE(AVG(accepted_swap.counterparty_rating),0) AS AVG_COUNTERPARTY_RATING
            FROM item
            LEFT JOIN accepted_swap ON item.item_number = accepted_swap.item_number_pro
            WHERE email = "{0}"
            '''.format(other_user)

            self.cursor.execute(rating)
            counter_rating = list(self.cursor.fetchall())[0]
            print('HERE ',counter_rating)
            base_table[i].append(counter_rating)

            distance = '''
            WITH users_cte AS (
            SELECT
            desired.email AS COUNTERPARTY
            ,proposed.email AS PROPOSER
            FROM swap
            LEFT JOIN item desired ON swap.item_number_counter = desired.item_number
            LEFT JOIN item proposed ON swap.item_number_pro = proposed.item_number
            WHERE swap.item_number_pro = "{0}" AND swap.item_number_counter = "{1}"
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
            '''.format(item_number_pro,item_number_counter)
            self.cursor.execute(distance)
            distance_value = self.cursor.fetchall()
            print("DISTANCE: ",distance_value)
            base_table[i].append(distance_value)

            i+=1


        return base_table


class SearchItems:

    def __init__(self, cursor):
        self.cursor = cursor

    def by_keyword(self, session, keyword):

        query_keywords = """
        SELECT Table_3.item_number AS "Item #", game_types.item_type AS 'Game type', Title, Table_3.Item_Condition AS 'Condition', Description, Table_3.Distance
        FROM
        (
        SELECT  item_number,Title,Item_Condition, Description, 
        round(3961 * (2 * ATAN2(SQRT(POW(SIN(RADIANS(counterparty_latitude - proposer_latitude)/2),2) + (COS(RADIANS(counterparty_latitude)) * COS(RADIANS(proposer_latitude))* 
        POW(SIN(RADIANS(counterparty_longitude - proposer_longitude)/2),2))), SQRT(1-POW(SIN(RADIANS(counterparty_latitude - proposer_latitude)/2),2) + (COS(RADIANS(counterparty_latitude)) * 
         COS(RADIANS(proposer_latitude)) * POW(SIN(RADIANS(counterparty_longitude - proposer_longitude)/2),2)))))) AS 'Distance'
        FROM (
        WITH pro_address AS( 
        SELECT user.email, address.longitude AS pro_long, address.latitude AS pro_lat
        FROM user
        LEFT JOIN address USING (postal_code)
        WHERE user.email LIKE %s
        ), counter_addresses AS (
        SELECT  table_1.item_number, user.email, title, item_description,item_condition, address.longitude  AS counter_long, address.latitude AS counter_lat FROM (
        SELECT  i.item_number, i.email, i.title, i.item_condition, i.item_description 
        FROM item i LEFT JOIN swap s ON i.item_number = s.item_number_counter OR i.item_number = s.item_number_pro
        WHERE (i.title LIKE %s OR i.item_description LIKE %s) AND
        s.swap_status IS NULL AND i.email NOT LIKE  %s) AS table_1 
        LEFT JOIN user  ON table_1.email = user.email
        LEFT JOIN address USING (postal_code)
        )
        SELECT counter_addresses.item_number AS item_number, counter_addresses.title AS Title, counter_addresses.item_condition AS Item_Condition, counter_addresses.item_description AS Description, pro_address.pro_long AS proposer_longitude, pro_address.pro_lat AS proposer_latitude, 
        counter_addresses.counter_long AS counterparty_longitude, counter_addresses.counter_lat AS counterparty_latitude
        FROM pro_address, counter_addresses) AS table_2 ORDER BY item_number ASC
        )
        AS Table_3 LEFT JOIN
        (
        SELECT item_number, 'computer_game' AS item_type FROM computer_game
        UNION SELECT item_number, 'video_game' AS item_type FROM video_game UNION
        SELECT item_number, 'card_game' AS item_type FROM card_game
        UNION
        SELECT item_number, 'board_game' AS item_type from board_game
        UNION
        SELECT item_number, 'jigsaw' AS item_type FROM jigsaw
        ) AS game_types USING (item_number);
                
        """

        self.cursor.execute(query_keywords, ('%'+session+'%', '%'+keyword+'%', '%'+keyword+'%', '%'+session+'%',))
        return self.cursor.fetchall()

    def by_my_postal_code(self, session):

        query_my_postal_code = """
        
        SELECT Table_1.item_number AS 'Item #', game_types.item_type AS 'Game type', Table_1.title AS Title, 
        Table_1.item_condition AS 'Condition', Table_1.item_description AS Description, 0 AS 'Distance'
        FROM
        (
        SELECT i.item_number,  i.title, i.item_condition, i.item_description FROM item i
        LEFT JOIN user ON i.email = user.email
        LEFT JOIN swap s ON i.item_number = s.item_number_counter
        WHERE s.swap_status IS NULL 
        AND user.postal_code = (SELECT postal_code FROM user WHERE user.email LIKE %s) AND 
        user.email NOT LIKE %s ORDER BY item_number ASC
        ) As Table_1
        LEFT JOIN ( SELECT item_number, 'computer_game' AS item_type
        FROM computer_game UNION SELECT item_number, 'video_game' AS item_type
        FROM video_game UNION SELECT item_number, 'card_game' AS item_type
        FROM card_game UNION
        SELECT item_number, 'board_game' AS item_type FROM board_game
        UNION SELECT item_number, 'jigsaw' AS item_type
        FROM jigsaw) AS game_types USING (item_number);



        """

        self.cursor.execute(query_my_postal_code, ('%'+session+'%', '%'+session+'%',))
        return self.cursor.fetchall()

    def by_distance(self, session, distance):

        query_distance = """
        
        SELECT Table_3.item_number AS 'Item #', game_types.item_type AS 'Game type', Title, Table_3.Item_Condition AS 'Condition', Description, Table_3.Distance
        FROM
        (
        SELECT  item_number,Title,Item_Condition, Description, 
        round(3961 * (2 * ATAN2(SQRT(POW(SIN(RADIANS(counterparty_latitude - proposer_latitude)/2),2) + (COS(RADIANS(counterparty_latitude)) * COS(RADIANS(proposer_latitude))* 
        POW(SIN(RADIANS(counterparty_longitude - proposer_longitude)/2),2))), SQRT(1-POW(SIN(RADIANS(counterparty_latitude - proposer_latitude)/2),2) + (COS(RADIANS(counterparty_latitude)) * 
         COS(RADIANS(proposer_latitude)) * POW(SIN(RADIANS(counterparty_longitude - proposer_longitude)/2),2)))))) AS 'Distance'
        FROM ( WITH pro_address AS( 
        SELECT user.email, address.longitude AS pro_long, address.latitude AS pro_lat
        FROM user LEFT JOIN address USING (postal_code)
        WHERE user.email LIKE %s), counter_addresses AS (SELECT  table_1.item_number, user.email, title, item_description,item_condition, address.longitude  AS counter_long, address.latitude AS counter_lat
        FROM (SELECT  i.item_number, i.email, i.title, i.item_condition, i.item_description
        FROM item i
        LEFT JOIN swap s ON i.item_number = s.item_number_counter OR i.item_number = s.item_number_pro WHERE s.swap_status IS NULL
        AND i.email NOT LIKE  %s) AS table_1 
        LEFT JOIN user  ON table_1.email = user.email
        LEFT JOIN address USING (postal_code)
        )
        SELECT counter_addresses.item_number AS item_number, counter_addresses.title AS Title, counter_addresses.item_condition AS Item_Condition, counter_addresses.item_description AS Description, pro_address.pro_long AS proposer_longitude, pro_address.pro_lat AS proposer_latitude, 
        counter_addresses.counter_long AS counterparty_longitude, counter_addresses.counter_lat AS counterparty_latitude
        FROM pro_address, counter_addresses) AS table_2
        ORDER BY item_number ASC
        )
        AS Table_3 LEFT JOIN
        (SELECT item_number, 'computer_game' AS item_type
        FROM computer_game UNION
        SELECT item_number, 'video_game' AS item_type FROM video_game
        UNION SELECT item_number, 'card_game' AS item_type
        FROM card_game UNION
        SELECT item_number, 'board_game' AS item_type
        FROM board_game
        UNION
        SELECT item_number, 'jigsaw' AS item_type
        FROM jigsaw) AS game_types
        USING (item_number)
        WHERE Table_3.Distance < %s;

        """

        self.cursor.execute(query_distance, ('%'+session+'%', '%'+session+'%', distance,))
        return self.cursor.fetchall()


    def by_postal_code(self, session, postal_code):

        query_postal_code = """
        SELECT Table_3.item_number AS 'Item #', game_types.item_type AS 'Game type', Title, Table_3.Item_Condition AS 'Condition', Description, Table_3.Distance
        FROM
        (
        SELECT  item_number,Title,Item_Condition, Description, 
        round(3961 * (2 * ATAN2(SQRT(POW(SIN(RADIANS(counterparty_latitude - proposer_latitude)/2),2) + (COS(RADIANS(counterparty_latitude)) * COS(RADIANS(proposer_latitude))* 
        POW(SIN(RADIANS(counterparty_longitude - proposer_longitude)/2),2))), SQRT(1-POW(SIN(RADIANS(counterparty_latitude - proposer_latitude)/2),2) + (COS(RADIANS(counterparty_latitude)) * 
         COS(RADIANS(proposer_latitude)) * POW(SIN(RADIANS(counterparty_longitude - proposer_longitude)/2),2)))))) AS 'Distance'
        FROM (WITH pro_address AS( 
        SELECT user.email, address.longitude AS pro_long, address.latitude AS pro_lat
        FROM user LEFT JOIN address USING (postal_code)
        WHERE user.email LIKE %s
        ), counter_addresses AS (
        SELECT  table_1.item_number, user.email, title, item_description,item_condition,address.postal_code, address.longitude  AS counter_long, address.latitude AS counter_lat
        FROM (
        SELECT  i.item_number, i.email, i.title, i.item_condition, i.item_description FROM item i
        LEFT JOIN swap s ON i.item_number = s.item_number_counter OR i.item_number = s.item_number_pro
        WHERE s.swap_status IS NULL AND i.email NOT LIKE %s
        ) 
        AS table_1 
        LEFT JOIN user ON table_1.email = user.email
        LEFT JOIN address USING (postal_code)
        WHERE address.postal_code LIKE %s
        )
        SELECT counter_addresses.item_number AS item_number, counter_addresses.title AS Title,
        counter_addresses.item_condition AS Item_Condition, counter_addresses.item_description AS Description, 
        pro_address.pro_long AS proposer_longitude, pro_address.pro_lat AS proposer_latitude, 
        counter_addresses.counter_long AS counterparty_longitude, counter_addresses.counter_lat AS counterparty_latitude
        FROM pro_address, counter_addresses) AS table_2
        ORDER BY item_number ASC
        )
        AS Table_3
        LEFT JOIN
        (
        SELECT item_number, 'computer_game' AS item_type
        FROM computer_game
        UNION
        SELECT item_number, 'video_game' AS item_type
        FROM video_game
        UNION
        SELECT item_number, 'card_game' AS item_type
        FROM card_game
        UNION
        SELECT item_number, 'board_game' AS item_type
        FROM board_game
        UNION
        SELECT item_number, 'jigsaw' AS item_type
        FROM jigsaw
        ) AS game_types
        USING (item_number)

        """

        self.cursor.execute(query_postal_code, ('%' + session + '%', '%' + session + '%', '%' + postal_code + '%',))
        return self.cursor.fetchall()


class ViewItem:
    def __init__(self, cursor):
        self.cursor = cursor

    def item_swap_availability(self, item_number):
        query_item_swap_availability = """
        SELECT swap_status
        FROM item i
        LEFT JOIN swap ON i.item_number = swap.item_number_pro
        OR i.item_number = swap.item_number_counter
        WHERE i.item_number LIKE %s
        """
        self.cursor.execute(query_item_swap_availability, (item_number,))
        return self.cursor.fetchall()[0]

    def item_owner_email(self, item_number):

        query_item_owner_email = """
        SELECT email FROM item i
        WHERE i.item_number LIKE %s
        """

        self.cursor.execute(query_item_owner_email, (item_number,))
        return self.cursor.fetchall()[0]

    def item_owner_nickname(self, owner):

        query_item_owner_nickname = """
        SELECT nickname from user u
        WHERE u.email LIKE %s
        """
        self.cursor.execute(query_item_owner_nickname, ('%' + owner + '%',))
        return self.cursor.fetchall()[0]

    def item_properties_current_user(self, item_number, session):

        query_item_properties_current_user = """
            
        SELECT table_1.item_number,table_1.title AS Title, Game_type.item_type AS 'Game type', video_game.platform_type AS platform, 
        video_game.media AS Media, table_1.item_condition AS 'Condition', jigsaw.piece_count AS 'Number of pieces', computer_game.os AS 'OS'
        FROM (
        SELECT *
        FROM item i
        LEFT JOIN swap ON i.item_number = swap.item_number_pro
        OR i.item_number = swap.item_number_counter
        WHERE i.item_number = %i 
        AND i.email = %s) AS table_1
        LEFT JOIN
        (
        SELECT item_number, 'computer_game' AS item_type
        FROM computer_game
        UNION
        SELECT item_number, 'video_game' AS item_type
        FROM video_game
        UNION
        SELECT item_number, 'card_game' AS item_type
        FROM card_game
        UNION
        SELECT item_number, 'board_game' AS item_type
        FROM board_game
        UNION
        SELECT item_number, 'jigsaw' AS item_type
        FROM jigsaw
        ) AS Game_type
        USING (item_number)
        LEFT JOIN video_game
        USING (item_number)
        LEFT JOIN computer_game
        USING (item_number)
        LEFT JOIN card_game
        USING (item_number)
        LEFT JOIN board_game
        USING (item_number)
        LEFT JOIN jigsaw
        USING (item_number);

        """

        self.cursor.execute(query_item_properties_current_user, ( item_number, '%' + session + '%', ))
        return self.cursor.fetchall()

    def item_properties_other_user(self,session, item_number,other_user):

        query_item_properties_other_user = """
        SELECT table_2.item_number AS 'Item #',table_2.title AS Title,item_type AS 'Game type', 
        platform_type AS Platform, media AS media, item_condition AS 'Condition', piece_count AS 'Number of Pieces', os AS OS, city AS City, state AS State, postal_code AS 'Postal code',
        round(3961 * (2 * ATAN2(SQRT(POW(SIN(RADIANS(counterparty_latitude - proposer_latitude)/2),2) + (COS(RADIANS(counterparty_latitude)) * COS(RADIANS(proposer_latitude))* 
        POW(SIN(RADIANS(counterparty_longitude - proposer_longitude)/2),2))), SQRT(1-POW(SIN(RADIANS(counterparty_latitude - proposer_latitude)/2),2) + (COS(RADIANS(counterparty_latitude)) * 
         COS(RADIANS(proposer_latitude)) * POW(SIN(RADIANS(counterparty_longitude - proposer_longitude)/2),2)))))) AS 'Distance'
        -- counterparty_longitude, counterparty_latitude,proposer_longitude, proposer_latitude
        FROM
        (
        WITH proposer AS 
        (
        SELECT address.longitude AS proposer_longitude, address.latitude AS proposer_latitude
        FROM user
        LEFT JOIN address USING (postal_code)
        WHERE user.email LIKE %s
        ),
        counter AS
        (
        SELECT *
        FROM (
        SELECT *
        -- i.item_number,i.title
        FROM item i
        LEFT JOIN swap ON i.item_number = swap.item_number_pro
        OR i.item_number = swap.item_number_counter
        LEFT JOIN user USING (email)
        LEFT JOIN address USING (postal_code)
        WHERE i.item_number LIKE %s
        AND i.email LIKE %s
        ) AS table_1
        LEFT JOIN
        (
        SELECT item_number, 'computer_game' AS item_type
        FROM computer_game
        UNION
        SELECT item_number, 'video_game' AS item_type
        FROM video_game
        UNION
        SELECT item_number, 'card_game' AS item_type
        FROM card_game
        UNION
        SELECT item_number, 'board_game' AS item_type
        FROM board_game
        UNION
        SELECT item_number, 'jigsaw' AS item_type
        FROM jigsaw
        ) AS Game_type
        USING (item_number)
        LEFT JOIN video_game
        USING (item_number)
        LEFT JOIN computer_game
        USING (item_number)
        LEFT JOIN card_game
        USING (item_number)
        LEFT JOIN board_game
        USING (item_number)
        LEFT JOIN jigsaw
        USING (item_number)
        )
        SELECT counter.email, counter.item_number,counter.title, counter.item_type, 
        counter.platform_type, counter.media, counter.item_condition, counter.piece_count, counter.os, counter.city, counter.state, counter.postal_code,
        counter.longitude AS counterparty_longitude, counter.latitude AS counterparty_latitude, proposer.proposer_longitude AS proposer_longitude, proposer.proposer_latitude AS proposer_latitude
        FROM counter, proposer
        ) AS table_2;
        
        """
        self.cursor.execute(query_item_properties_other_user, ('%' + session + '%', '%' + item_number + '%', '%' + other_user + '%',))
        return self.cursor.fetchall()

    def item_owner_rating(self, owner):

        query_owner_rating = """
        SELECT (SUM(proposer_rating) + SUM(counterparty_rating)) / 
        (COUNT(proposer_rating) + COUNT(counterparty_rating)) AS total_rating 
        FROM accepted_swap AS acc 
        LEFT JOIN swap AS a ON acc.item_number_pro = a.item_number_pro 
        LEFT JOIN item AS b ON b.item_number = a.item_number_pro 
        LEFT JOIN user AS p ON p.email = b.email 
        LEFT JOIN swap AS c ON acc.item_number_counter = c.item_number_counter 
        LEFT JOIN item AS d ON d.item_number = c.item_number_counter 
        LEFT JOIN user AS w ON w.email = d.email 
        WHERE p.email LIKE %s OR w.email LIKE %s

        """
        self.cursor.execute(query_owner_rating, ('%' + owner + '%', '%' + owner + '%',))
        return self.cursor.fetchall()[0]

    def current_user_unaccepted_swaps(self, session):
        query_user_unaccepted_swaps = """
        SELECT COUNT(swap_status) FROM user 
        LEFT JOIN item ON item.email = user.email 
        LEFT JOIN swap ON swap.item_number_counter = item.item_number 
        WHERE user.email LIKE %s AND swap_status = 'pending'
        """
        self.cursor.execute(query_user_unaccepted_swaps, ('%' + session + '%',))
        return self.cursor.fetchall()[0]

    def current_user_unrated_swaps(self, session):
        query_user_unrated_swaps = """
        SELECT (COUNT(proposer_rating) + COUNT(counterparty_rating)) AS unrated_swaps 
        FROM accepted_swap AS acc 
        LEFT JOIN swap AS a ON acc.item_number_pro = a.item_number_pro 
        LEFT JOIN item AS b ON b.item_number = a.item_number_pro 
        LEFT JOIN user AS p ON p.email = b.email 
        LEFT JOIN swap AS c ON acc.item_number_counter = c.item_number_counter 
        LEFT JOIN item AS d ON d.item_number = c.item_number_counter 
        LEFT JOIN user AS w ON w.email = d.email 
        WHERE proposer_rating IS NULL OR counterparty_rating IS NULL AND (p.email LIKE %s  OR w.email LIKE %s)
        """
        self.cursor.execute(query_user_unrated_swaps, ('%' + session + '%','%' + session + '%',))
        return self.cursor.fetchall()[0]

class MyItemsForm:

    def __init__(self, cursor):
        self.cursor = cursor

    def display_inventory_count(self, session):
        query_inventory_count = "SELECT \
        COUNT(board_game.item_number) AS 'Board games', \
        COUNT(card_game.item_number) AS 'Card games', \
        COUNT(computer_game.item_number) AS 'Computer games', \
        COUNT(jigsaw.item_number) AS 'Jigsaw puzzles', \
        COUNT(video_game.item_number) AS 'Video Games', \
        COUNT(board_game.item_number) + COUNT(card_game.item_number) + COUNT(computer_game.item_number) + COUNT(jigsaw.item_number)  + COUNT(video_game.item_number)  AS Total \
        FROM user JOIN item USING(email) \
        LEFT JOIN swap ON item.item_number = swap.item_number_pro OR item.item_number = swap.item_number_counter \
        LEFT JOIN card_game USING(item_number) \
         LEFT JOIN board_game USING(item_number) \
        LEFT JOIN computer_game USING(item_number) \
        LEFT JOIN video_game USING(item_number) \
        LEFT JOIN jigsaw USING(item_number) \
        WHERE email = %(session)s AND swap.swap_status IS NULL"
        self.cursor.execute(query_inventory_count, {'session': session})
        return self.cursor.fetchall()[0]

    def display_inventory_table(self, session):
        query_inventory = "SELECT table_1.item_number,table_1.title AS Title, Game_type.item_type AS 'Game type', table_1.item_condition AS 'Condition', table_1.item_description \
        FROM ( \
        SELECT * \
        FROM item i \
        LEFT JOIN swap ON i.item_number = swap.item_number_pro OR i.item_number = swap.item_number_counter WHERE \
        swap.swap_status IS NULL ) AS table_1 LEFT JOIN \
        (\
        SELECT item_number, 'Computer game' AS item_type FROM computer_game \
        UNION \
        SELECT item_number, 'Video game' AS item_type FROM video_game \
        UNION \
        SELECT item_number, 'Card game' AS item_type FROM card_game \
        UNION \
        SELECT item_number, 'Board game' AS item_type FROM board_game\
        UNION  \
        SELECT item_number, 'Jigsaw puzzle' AS item_type FROM jigsaw\
        ) AS Game_type\
        USING (item_number)\
        LEFT JOIN video_game\
        USING (item_number)\
        LEFT JOIN computer_game\
        USING (item_number)\
        LEFT JOIN card_game\
        USING (item_number)\
        LEFT JOIN board_game\
        USING (item_number)\
        LEFT JOIN jigsaw\
        USING (item_number) \
        WHERE email = %(session)s"
        self.cursor.execute(query_inventory, {'session': session})
        return self.cursor.fetchall()

class ListItemForm:
    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db

    # Get game types
    def show_game_types(self, session):
        query_item_type = "SELECT DISTINCT item_type \
        FROM ( \
        SELECT item_number, 'Computer game' AS item_type \
        FROM computer_game \
        UNION \
        SELECT item_number, 'Video game' AS item_type \
        FROM video_game \
        UNION \
        SELECT item_number, 'Card game' AS item_type \
        FROM card_game \
        UNION \
        SELECT item_number, 'Board game' AS item_type \
        from board_game \
        UNION \
        SELECT item_number, 'Jigsaw puzzle' AS item_type \
        FROM jigsaw \
        ) AS Game_type"

        self.cursor.execute(query_item_type, {'session': session})
        return self.cursor.fetchall()

    # Get platform types for video games from database
    def show_video_game_platform_type(self, session):
        query_video_game_type = "SELECT type from video_platform"
        self.cursor.execute(query_video_game_type, {'session': session})
        return self.cursor.fetchall()

    # Get platform types for computer games
    def show_media_type(self, session):
        return ['linux', "mac", "windows"]

    # Get media types for video games
    def show_video_game_media_type(self, session):
        return ['optical disc', 'game card', 'cartridge']

    # Get condition options
    def show_item_condition(self, session):
        return ['Mint', 'Like New', 'Lightly Used', 'Moderately Used', 'Heavily Used', 'Damaged/Missing Parts']

    # Retrieve number of unaccepted swaps
    def display_unaccepted_swaps(self, session):
        query_unaccepted_swaps = "SELECT COUNT(swap_status) FROM user \
        LEFT JOIN item ON item.email = user.email \
        LEFT JOIN swap ON swap.item_number_counter = item.item_number \
        WHERE user.email = %(session)s AND swap_status = 'pending'"
        self.cursor.execute(query_unaccepted_swaps, { 'session': session})
        return self.cursor.fetchall()[0]

    # Get number of unrated swaps
    def display_unrated_swaps(self, session):
        query_unrated_swaps = "SELECT (COUNT(proposer_rating) + COUNT(counterparty_rating)) AS unrated_swaps \
        FROM accepted_swap AS acc \
        LEFT JOIN swap AS a ON acc.item_number_pro = a.item_number_pro \
        LEFT JOIN item AS b ON b.item_number = a.item_number_pro \
        LEFT JOIN user AS p ON p.email = b.email \
        LEFT JOIN swap AS c ON acc.item_number_counter = c.item_number_counter \
        LEFT JOIN item AS d ON d.item_number = c.item_number_counter \
        LEFT JOIN user AS w ON w.email = d.email \
        WHERE proposer_rating IS NULL OR counterparty_rating IS NULL AND (p.email = %(session)s OR w.email = %(session)s)"
        self.cursor.execute(query_unrated_swaps, { 'session': session})
        return self.cursor.fetchall()[0]

    def insert_card_game(self, email, title, item_condition, item_description):
        insert_item = "INSERT INTO item (email, title, item_condition, item_description) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_item, (email, title, item_condition, item_description))
        item_number = self.cursor.lastrowid
        insert_card = " INSERT INTO card_game (item_number) VALUES (LAST_INSERT_ID())"
        self.cursor.execute(insert_card)
        self.db.commit()
        return item_number


    def insert_board_game(self, email, title, item_condition, item_description):
        insert_item = "INSERT INTO item (email, title, item_condition, item_description) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_item, (email, title, item_condition, item_description))
        item_number = self.cursor.lastrowid
        insert_board_game = "INSERT INTO board_game (item_number) VALUES (LAST_INSERT_ID())"
        self.cursor.execute(insert_board_game)
        self.db.commit()
        return item_number

    def insert_item_jigsaw(self, email, title, item_condition, item_description, piece_count):
        insert_item = "INSERT INTO item (email, title, item_condition, item_description) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_item, (email, title, item_condition, item_description))
        item_number = self.cursor.lastrowid
        insert_jigsaw = " INSERT INTO jigsaw (item_number, piece_count) VALUES (LAST_INSERT_ID(), %(piece_count)s)"
        self.cursor.execute(insert_jigsaw,  { 'piece_count': piece_count})
        self.db.commit()
        return item_number

    def insert_item_computer_game(self, email, title, item_condition, item_description, computer_game_platform):
        insert_item = "INSERT INTO item (email, title, item_condition, item_description) VALUES (%s, %s, %s, %s);"
        self.cursor.execute(insert_item, (email, title, item_condition, item_description))
        item_number = self.cursor.lastrowid
        insert_game = " INSERT INTO computer_game (item_number, os) VALUES (LAST_INSERT_ID(), 'windows')"
        self.cursor.execute(insert_game, {'os': computer_game_platform})
        self.db.commit()
        return item_number

    def insert_item_video_game(self, email, title, item_condition, item_description, platform, media):
        insert_item = "INSERT INTO item (email, title, item_condition, item_description) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_item, (email, title, item_condition, item_description))
        item_number = self.cursor.lastrowid
        insert_statement = "INSERT INTO video_game (item_number, platform_type, media) VALUES (LAST_INSERT_ID(), %(platform)s, %(media)s)"
        self.cursor.execute(insert_statement,{'platform': platform, 'media': media})
        self.db.commit()
        return item_number


class ProposeSwapForm:

    def __init__(self, cursor,db):
        self.cursor = cursor
        self.db = db

    def get_target_item_name(self,target_item_number):
        get_target_item_name_query = " \
        select title from item where item_number = %s "
        self.cursor.execute(get_target_item_name_query,(target_item_number,))
        table_element =self.cursor.fetchall()
        
       # table_head = [x[0] for x in self.cursor.description]
        return (table_element)

    def get_user_own_inventory(self,user_email):
        get_user_inventory = """
        with pending_or_accepted_item as  (select item_number, email, count(swap_status) as notava from item,swap where item_number in (item_number_pro,item_number_counter) 
        and email = %s and  swap_status in ('pending','accepted') group by item_number
        )
		select item_number as 'Item #',
        (case  when exists(select * from board_game where item_number = i.item_number) then 'Board Game'
        when exists(select * from computer_game where item_number = i.item_number) then 'Computer Game'
        when exists(select * from video_game where item_number = i.item_number) then 'Video Game'
        when exists(select * from card_game where item_number = i.item_number) then 'Card Game'
        when exists(select * from jigsaw where item_number = i.item_number) then 'Jigsaw'
        else null 
        end) as 'Game Type',
        title as Title,item_condition as 'Condition' from item i left join pending_or_accepted_item using(item_number)
        where i.email = %s and notava is null
        """	
        print(user_email)
        self.cursor.execute(get_user_inventory,(user_email,user_email))
        table_element = self.cursor.fetchall()
        table_head = [x[0] for x in self.cursor.description]
        return (table_head,table_element)
    def insert_new_swap(self,item_number_pro,item_number_con):
        insert_swap_query = """
        INSERT INTO swap VALUES(%s,%s,"pending",now())
        """
        self.cursor.execute(insert_swap_query,(item_number_pro,item_number_con))
        self.db.commit()

class SwapHistoryForm:

    def __init__(self, cursor,db):
        self.cursor = cursor
        self.db = db

    def update_rating(self,item_pro,item_con,rating,myrole):

        
        update_rating_query_pro2con = """
        UPDATE accepted_swap
        SET counterparty_rating = %s
        WHERE item_number_pro = %s AND item_number_counter = %s
        """

        update_rating_query_con2pro = """
        UPDATE accepted_swap
        SET proposer_rating = %s
        WHERE item_number_pro = %s AND item_number_counter = %s
        """
        if myrole == 'proposer': 
            self.cursor.execute(update_rating_query_pro2con,(rating,item_pro,item_con))
            self.db.commit()

        elif myrole =='counterparty':
            
            self.cursor.execute(update_rating_query_con2pro,(rating,item_pro,item_con))
            self.db.commit()
            
        else:
            print("debug error in update rating def")



    def show_current_user_swap_stats(self,user_email):
        user_swap_stat_query ="""
            with current_user_swap as (select *,'proposer' as role from swap left join item on swap.item_number_pro = item.item_number
            left join user using(email)
            where email = %s
            union 
            select *, 'counterparty' as role from swap left join item on swap.item_number_counter = item.item_number
            left join user using(email)
            where email = %s)
            select role as Role,count(swap_status) as Total,
            sum(case when swap_status = 'accepted' then 1 else 0 end) as Accepted, 
            sum(case when swap_status = 'rejected' then 1 else 0 end) as Rejected,
            round(100*sum(case when swap_status = 'rejected' then 1 else 0 end)/count(*),1) as 'Rejected Rate'

            from current_user_swap group by role
            """
        self.cursor.execute(user_swap_stat_query,(user_email,user_email))
        table_element = self.cursor.fetchall()
        table_column_name=[x[0] for x in self.cursor.description]
        return(table_column_name,table_element)

    def show_current_user_all_swap_history(self,user_email):
        all_swap_history_query = """
            with current_user_swap as (select *,'proposer' as role from swap left join item on swap.item_number_pro = item.item_number
            left join user using(email)
            where email = %s
            union 
            select *, 'counterparty' as role from swap left join item on swap.item_number_counter = item.item_number
            left join user using(email)
            where email = %s)
            select item_number_pro,item_number_counter,propose_date as 'Proposed Date', swap_status as 'Swap Status',role as 'My Role',
            pro.title as 'Proposed Item',con.title as 'Desired Item',
            case when current_user_swap.item_number = current_user_swap.item_number_pro then 
            (select nickname from user join item using(email) 
            where item.item_number = current_user_swap.item_number_counter)
            when current_user_swap.item_number = current_user_swap.item_number_counter then
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
            order by propose_date asc
            """
        self.cursor.execute(all_swap_history_query,(user_email,user_email))
        table_element = self.cursor.fetchall()
        table_column_name=[x[0] for x in self.cursor.description]
        return(table_column_name,table_element)
    
class SwapDetailsForm:
    def __init__(self, cursor,db):
        self.cursor = cursor
        self.db = db

    def remove_none_head_and_elements(self,input_tuple_head,input_list_element):
        #return turple of lists, remove all nones regard less the ttile name,
        #may change to remove certain head names instead
        column_name_no_none=[]
        elements_no_none =[]

        for index, item in enumerate(input_list_element):
            if item != None :
                column_name_no_none.append(input_tuple_head[index])
                elements_no_none.append(item)
        
        return(column_name_no_none,elements_no_none)

    def form1_swapdetails(self,current_user_email,item_pro,item_con):

        swapdetails_query = """
            with temp_swap_tb as (
            select *, case when item_number_pro is null then 'owner' 
            else 'proposer' end as myrole 
                from user join item using (email)
                join swap on item.item_number = swap.item_number_pro 
                where email = %s
                union
                select *,case when item_number_pro is null then 'owner' 
            else 'counterparty' end as myrole  
            from user join item using (email)
                join swap on item.item_number = swap.item_number_counter 
                where email = %s
            

            )
            select 
            propose_date as 'Proposal Date',
            case when accepted_date = null then rejected_date 
            else accepted_date end as 'Accpeted/Rejected Date',

            case when (accepted_date is null and rejected_date is null) then 'Pending'
            when  (accepted_date is null and rejected_date is not null) then 'Rejected'
            else  'Accepted' end as Status,
            myrole as 'My Role',
            case when (myrole = 'proposer') then counterparty_rating 
            else proposer_rating end as 'Rating Left'
            from temp_swap_tb left join accepted_swap using(item_number_pro) left join rejected_swap using(item_number_pro)
            where temp_swap_tb.item_number_pro = %s and temp_swap_tb.item_number_counter = %s
            """

        self.cursor.execute(swapdetails_query,(current_user_email,current_user_email,item_pro,item_con))
        table_element = self.cursor.fetchall()
        table_column_name=[x[0] for x in self.cursor.description]
        return(table_column_name,table_element)
    
    def other_user(self,item_number_pro,item_number_con,my_item_number):

        swap_history_form2_query = """
            WITH users_cte AS (
            SELECT desired.email AS COUNTERPARTY, proposed.email AS PROPOSER
            FROM swap
            LEFT JOIN item desired ON swap.item_number_counter = desired.item_number
            LEFT JOIN item proposed ON swap.item_number_pro = proposed.item_number
            WHERE swap.item_number_pro = %s
            AND  swap.item_number_counter = %s
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
            
            SELECT nickname,round(distance.distance,2) as Distance,first_name as Name,email as Email,phone_number as Phone,phone_type,is_shared
            from user join item using(email) left join phone using(email)
            LEFT JOIN distance ON 1=1 
            where item_number = %s
            """

        if str(my_item_number) == item_number_pro:
            
            self.cursor.execute(swap_history_form2_query,(item_number_pro,item_number_con,item_number_con))
        elif str(my_item_number)== item_number_con:
            
            self.cursor.execute(swap_history_form2_query,(item_number_pro,item_number_con,item_number_pro))
        
        table_element = self.cursor.fetchall()
        table_column_name=[x[0] for x in self.cursor.description]
        return(table_column_name,table_element)
    
    def form34_item_details(self,item_pro,item_con):
        item_detail_query = """
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
        LEFT JOIN jigsaw USING (item_number) where item_number = %s
            """
        
        self.cursor.execute(item_detail_query,(item_pro,))
        propose_item_element = self.cursor.fetchall()
        propose_item_column_name = [x[0] for x in self.cursor.description]
  
        


        self.cursor.execute(item_detail_query,(item_con,))
        desired_item_element = self.cursor.fetchall()
        desired_item_column_name = [x[0] for x in self.cursor.description]

      
   
        
        return(propose_item_column_name,propose_item_element,desired_item_column_name,desired_item_element)

