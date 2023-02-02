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

	def register_phone_number(self, phone_number, email, phone_type, is_shared):
		self.cursor.execute(
			"INSERT INTO phone (phone_number, email, phone_type, is_shared) VALUES (%s, %s, %s, %s)"
			(phone_number, email, phone_type, share_phone_number)
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



