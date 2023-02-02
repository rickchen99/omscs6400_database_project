import functools
import traceback
import time
from flaskr.app_functions import UserRegistrationForm, LoginForm, MainMenuForm
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('gameswap', __name__, url_prefix='/gameswap')

# Registration and Authentication

@bp.route('/register', methods=('GET', 'POST'))
def register():
    phone_type_choices = ['home', 'work', 'mobile']
    if request.method == 'POST':
    	phone_number = None
    	email = request.form['email']
    	password = request.form['password']
    	nickname = request.form['nickname']
    	first_name = request.form['first_name']
    	last_name = request.form['last_name']
    	postal_code = request.form['postal_code']
    	# phone_number = request.form['phone_number'] #To do: Incorporate phone functionality
    	# phone_type = requeust.form['phone_type'] #To do: Incorporate phone functionality
    	# share_phone_number = requuest.form['share_phone_number'] #To do: Incorporate phone functionality
    	db = get_db()
    	cursor = db.cursor(buffered=True)
    	register = UserRegistrationForm(cursor, db)
    	error = None

        # All fields below are required

    	if not email:
    		error = 'Email is required.'
    	elif not password:
    		error = 'Password is required.'
    	elif not nickname:
    		error = 'Nickname is required.'
    	elif not first_name:
    		error = 'First Name is required.'
    	elif not last_name:
    		error = 'Last Name is required.'
    	elif not postal_code:
    		error = 'Postal Code is required.'

        # If all fields have been filled out, proceed with login attempt.

    	if error is None:
    		try:
    			register.register_user(email, nickname, password, first_name, last_name, postal_code)

    			if phone_number is not None:
    				register.register_phone_number(phone_number, email, phone_type, is_shared)

    		except Exception as e:
    			error = f"There was an error with the registration: {e}" # This needs to change. Printing error for troubleshooting for now.

    		else:
    			flash("You have successfully registered. Please log in to continue.")
    			return redirect(url_for("gameswap.login"))

    	if error is not None:
    		flash(error)

    return render_template('auth/register.html', phone_type_choices=phone_type_choices) 

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        login_attempt = request.form['login_attempt']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor(buffered=True)
        log_in = LoginForm(cursor)
        error = None
        login_user = None

        # Try email for login if provided. If phone is provided, try phone instead.
        # If pw is incorrect at any point, throw error.

        try:
        	login_user = log_in.email_login_attempt(login_attempt)
        	if login_user[1] != password:
        		error = 'Password is incorrect'
        except:
        	try:
        		login_user = log_in.phone_login_attempt(login_attempt)
        		if login_user[1] != password:
        			error = 'Password is incorrect'
        	except:
        		error = 'Account not found'

            # If valid email or phone is provided with valid pw, grab email to be used as session variable.   

        if error is None:
            session.clear()
            session['user_id'] = login_user[0]
            flash("You have successfully logged in!")
            return redirect(url_for('gameswap.main_menu'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
    	g.user = get_db()
    	cursor = g.user.cursor(buffered=True)
    	cursor.execute(
		'SELECT email FROM user WHERE email = %s', (user_id,))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('gameswap.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('gameswap.login'))

        return view(**kwargs)

    return wrapped_view

# Function for each form

@bp.route('/mainmenu', methods=('GET', 'POST'))
def main_menu():
    db = get_db()
    cursor = db.cursor(buffered=True)
    menu_items = MainMenuForm(cursor)
    welcome_message = menu_items.welcome_message(session['user_id'])
    my_rating = menu_items.display_my_rating(session['user_id'])[0]
    if my_rating is not None:
        my_rating = round(my_rating, 2)
    unaccepted_swaps = menu_items.display_unaccepted_swaps(session['user_id'])[0]
    unrated_swaps = menu_items.display_unrated_swaps(session['user_id'])[0]
    return render_template('forms/mainmenu.html', welcome_message=welcome_message, \
    my_rating=my_rating, unaccepted_swaps=unaccepted_swaps, unrated_swaps=unrated_swaps)

@bp.route('/listitem', methods=('GET', 'POST'))
def list_item():
    db = get_db()
    return render_template('forms/listitem.html')

@bp.route('/myitems', methods=('GET', 'POST'))
def my_items():
    db = get_db()
    return render_template('forms/myitems.html')

@bp.route('/searchitems', methods=('GET', 'POST'))
def search_items():
    db = get_db()
    return render_template('forms/searchitems.html')

@bp.route('/viewitems', methods=('GET', 'POST'))
def view_items():
    db = get_db()
    return render_template('forms/viewitems.html')

@bp.route('/proposeswap', methods=('GET', 'POST'))
def propose_swap():
    db = get_db()
    return render_template('forms/proposeswap.html')

@bp.route('/acceptrejectswap', methods=('GET', 'POST'))
def accept_reject_swap():
    db = get_db()
    return render_template('forms/acceptrejectswap.html')

@bp.route('/rateswaps', methods=('GET', 'POST'))
def rate_swaps():
    db = get_db()
    return render_template('forms/rateswaps.html')

@bp.route('/swaphistory', methods=('GET', 'POST'))
def swap_history():
    db = get_db()
    return render_template('forms/swaphistory.html')

@bp.route('/swapdetails', methods=('GET', 'POST'))
def swap_details():
    db = get_db()
    return render_template('forms/swapdetails.html')

@bp.route('/updateuserinfo', methods=('GET', 'POST'))
def update_user_info():
    db = get_db()
    return render_template('forms/updateuserinfo.html')