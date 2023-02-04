import functools
from posixpath import split
import traceback
import time
import argparse
from flaskr.app_functions import UserRegistrationForm, LoginForm, MainMenuForm, RateSwapForm, AcceptRejectForm, ViewItem, SearchItems, ListItemForm, MyItemsForm,UpdateUserInfoForm,SwapDetailsForm,SwapHistoryForm,ProposeSwapForm
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('gameswap', __name__, url_prefix='/gameswap')

# Registration and Authentication

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        nickname = request.form['nickname']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        postal_code = request.form['postal_code']
        if request.form['phone_number'] == "":
            phone_number = None
        else:
            phone_number = request.form['phone_number']
        if request.form['phone_type'] == "":
            phone_type = None
        else:
            phone_type = request.form['phone_type']
        try:
            share_phone_number = request.form['share_phone_number']
        except:
            share_phone_number = '0'
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
                    register.register_phone_number(phone_number, email, phone_type, share_phone_number)

            except Exception as e:
                error = f"There was an error with the registration: {e}{traceback.format_exc()}" # This needs to change. Printing error for troubleshooting for now.

            else:
                flash("You have successfully registered. Please log in to continue.")
                return redirect(url_for("gameswap.login"))

        if error is not None:
            flash(error)

    return render_template('auth/register.html') 

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
    over_five_days_check = menu_items.unaccepted_swaps_over_five_days(session['user_id'])[0]
    unrated_swaps = menu_items.display_unrated_swaps(session['user_id'])[0]
    return render_template('forms/mainmenu.html', welcome_message=welcome_message, \
    my_rating=my_rating, unaccepted_swaps=unaccepted_swaps, unrated_swaps=unrated_swaps,
    over_five_days_check=over_five_days_check)


@bp.route('/updateuserinfo', methods=('GET', 'POST'))
def update_user_info():
    db = get_db()
    cursor = db.cursor(buffered=True)
    my_info_items = UpdateUserInfoForm(cursor, db)
    if (my_info_items.allow_update_access_swaps(session['user_id'])[0] > 0) and (my_info_items.allow_update_access_rating(session['user_id'])[0] > 0):
        flash(f'You are not allowed to make any information updates due to unapproved swaps and unrated swaps.\n'
            'All unapproved swaps will need to be completed and unrated swaps rated in order for this feature to be enabled.')
        return redirect(url_for('gameswap.main_menu'))
    elif my_info_items.allow_update_access_swaps(session['user_id'])[0] > 0:
        flash(f'You are not allowed to make any information updates due to unapproved swaps.\n'
            'All unapproved swaps will need to be completed in order for this feature to be enabled.')
        return redirect(url_for('gameswap.main_menu'))
    elif my_info_items.allow_update_access_rating(session['user_id'])[0] > 0:
        flash(f'You are not allowed to make any information updates due to unrated swaps.\n'
            'All unrated swaps will need to be rated in order for this feature to be enabled.')
        return redirect(url_for('gameswap.main_menu'))
    else:
        show_my_info = my_info_items.display_my_info(session['user_id'])

        if request.method == 'POST':
            if request.form['password'] == "":
                pass
            else:
                my_info_items.update_password(request.form['password'], session['user_id'])

            if request.form['nickname'] == "":
                pass
            else:   
                my_info_items.update_nickname(request.form['nickname'], session['user_id'])

            if request.form['first_name'] == "":
                pass
            else:
                my_info_items.update_first_name(request.form['first_name'], session['user_id'])

            if request.form['last_name'] == "":
                pass
            else:    
                my_info_items.update_last_name(request.form['last_name'], session['user_id'])

            if request.form['postal_code'] == "":
                pass
            else:
                my_info_items.update_postal_code(request.form['postal_code'], session['user_id'])

            try:
                if request.form['phone_number'] == "":
                    pass
                else:
                    my_info_items.update_phone_number(request.form['phone_number'], session['user_id'])              
            except:
                flash("This phone number is already in use!")
                return render_template('forms/updateuserinfo.html', show_my_info=show_my_info)

            if "Current" in request.form['phone_type']:
                pass
            else:
                my_info_items.update_phone_type(request.form['phone_type'], session['user_id'])

            try:
                my_info_items.update_is_shared(request.form['share_phone_number'], session['user_id'])
            except:
                user_share_phone_number = '0'
                my_info_items.update_is_shared(user_share_phone_number, session['user_id'])

            show_my_info = my_info_items.display_my_info(session['user_id'])

            flash("Information updated successfully!")

        return render_template('forms/updateuserinfo.html', show_my_info=show_my_info)

# Rate Swaps
@bp.route('/rateswaps', methods=('GET', 'POST'))
def rate_swaps():
    db = get_db()

    cursor = db.cursor(buffered=True)
    form = RateSwapForm(cursor)

    is_empty = False
    cols = ['Acceptance Date','My role','Proposed Item','Desired Item','Other User','Rating']
    table = list(form.display_table(session['user_id']))
    if table is None or table == []:
        table = 'No unrated swaps found.'
        is_empty = True
    print('TABLE ',table)

    if request.method == 'POST':
        if request.form['rating'] == "":
            pass
        else:
            rating = int(request.form['rating'])
            rownum = int(request.form['rownum'].replace("<Namespace {'value': ",'').replace("}>",''))
            row = table[rownum]
            print("SELECTED ROW: ",row)
            print(rating,row[1],row[6],row[7])
            form.update_rating(rating,row[1],row[6],row[7])
            table = list(form.display_table(session['user_id']))
            if table is None or table == []:
                table = 'No unrated swaps found.'
                is_empty = True
    print('TABLE2 ',table)
    # TODO update statement not wokring right on battlefield - NBA role


    return render_template('forms/rateswaps.html',cols = cols,is_empty=is_empty,table=table)


# Accept Reject Swaps
@bp.route('/acceptrejectswap', methods=('GET', 'POST'))
def accept_reject_swap():
    db = get_db()
    cursor = db.cursor(buffered=True)
    items = AcceptRejectForm(cursor)
    cols = ['Date','Desired Item','Proposer','Rating','Distance','Proposed Item','']
    table = items.fetch_swaps(session['user_id'])

    is_empty = False
    if table is None or table == []:
        table = 'No unrated swaps found.'
        is_empty = True
    print('TABLE ',table)

    return render_template('forms/acceptrejectswap.html',cols=cols,is_empty=is_empty,table = table)

@bp.route('/searchitems', methods=('GET', 'POST'))
def search_items():

    if request.method == 'POST':

        search_value_keyword = request.form['keyword']
        search_value_my_postal_code = request.form['my_postal_code']
        search_value_distance = request.form['distance']
        search_value_postal_code = request.form['postal_code']

        if search_value_keyword:
            return search_results(search_value_keyword)

        elif search_value_my_postal_code:
            return search_results(search_value_my_postal_code)

        elif search_value_distance:
            return search_results(search_value_distance)

        else:
            return search_results(search_value_postal_code)       

    return render_template('forms/searchitems.html')

@bp.route('/searchresults', methods=('GET', 'POST'))
def search_results(search):

    db = get_db()
    cursor = db.cursor(buffered=True)
    items = SearchItems(cursor)

    #if request.method == 'POST':
    #item_number_test = request.form['item_number']
    #print(item_number_test)


    if request.form['keyword']:
        results = items.by_keyword(session=session['user_id'], keyword=search)

    elif request.form['postal_code']:
        results = items.by_postal_code(session=session['user_id'], postal_code=search)

    elif request.form['distance']:
        results = items.by_distance(session=session['user_id'], distance=search)

    else:
        results = items.by_my_postal_code(session=session['user_id'])


    if results:
        return render_template('forms/searchresults.html', results=results)
    else:
        flash('No results found!')
        return redirect(url_for('gameswap.search_items'))



@bp.route('/viewitems', methods=('GET', 'POST'))
def view_items():

    db = get_db()
    cursor = db.cursor(buffered=True)
    items = ViewItem(cursor)


    #item_number_test = request.form['item_number']

    # item number below should be updated to read from hyperlink
    selected_item_number = "24"

    item_swap_availability = items.item_swap_availability(item_number=selected_item_number)


    current_user = session['user_id']
    current_user_unaccepted_swaps = items.current_user_unaccepted_swaps(session=current_user)
    current_user_unrated_swaps = items.current_user_unrated_swaps(session=current_user)

    item_owner = items.item_owner_email(item_number=selected_item_number)

    item_owner_nickname = items.item_owner_nickname(item_owner[0])
    owner_rating = items.item_owner_rating(owner=item_owner[0])

    if current_user == item_owner:

        item_properties = items.item_properties_current_user(item_number=selected_item_number, session=current_user)
        # column_name = [x[0] for x in cursor.description]

        return render_template('forms/viewitems.html', item_owner=current_user, item_properties=item_properties,
                               current_user=current_user, current_user_unaccepted_swaps=current_user_unaccepted_swaps[0],
                               current_user_unrated_swaps=current_user_unrated_swaps[0],
                               item_swap_availability=item_swap_availability[0]
                               )
    else:

        item_properties = items.item_properties_other_user(session=current_user, item_number=selected_item_number,
                                                           other_user=item_owner[0])
        # column_name = [x[0] for x in cursor.description]

        return render_template('forms/viewitems.html', item_owner=item_owner[0], item_properties=item_properties,
                               current_user=current_user, owner_rating=owner_rating[0],
                               current_user_unaccepted_swaps=current_user_unaccepted_swaps[0],
                               current_user_unrated_swaps=current_user_unrated_swaps[0],
                               item_owner_nickname=item_owner_nickname[0],
                               item_swap_availability=item_swap_availability[0])

@bp.route('/listitem', methods=('GET', 'POST'))
def list_item():
    db = get_db()
    cursor = db.cursor(buffered=True)
    list_items = ListItemForm(cursor, db)
    # Get number of unaccepted swaps and unrated swaps
    # Get options for dropdown boxes for each game type
    game_type_options = list_items.show_game_types(session['user_id'])
    video_game_platform_types = list_items.show_video_game_platform_type(session['user_id'])
    video_game_media_types = list_items.show_video_game_media_type(session['user_id'])
    computer_game_platform_types = list_items.show_media_type(session['user_id'])

    # Get item conditions
    condition_types = list_items.show_item_condition(session['user_id'])

    if request.method == 'POST':
        # Retrieve form requests for common fields
        title = request.form['title']
        item_condition = request.form['item_condition']
        item_description = request.form['item_description']
        game_type = request.form['game_type']

        # Retrieve form requests for specific game types
        piece_count = request.form['jigsaw_dropdown']
        computer_game_platform = request.form['computer_game_platform_dropdown']
        video_game_platform = request.form['video_game_platform']
        video_game_media = request.form['video_game_media']
        error = False

        if game_type == '':
            flash("No game type selected. Select game type.")
            error = True
        if game_type == 'Jigsaw puzzle':
            if piece_count == '':
                flash("Insert a value for piece count.")
                error = True
            else:
                if int(piece_count) <= 0:
                    flash("Piece count cannot be negative. Insert a positive value.")
                    error = True
        if game_type == 'Computer game':
            if computer_game_platform == '':
                flash('Operating System not selected. Select an operating system for your game.')
                error = True
        if game_type == 'Video game':
            if video_game_platform == '':
                flash('Platform not selected. Select a platform for your video game.')
                error = True
            if video_game_media == '':
                flash('Media not selected. Select a media for your video game.')
                error = True
        if item_condition == '':
            flash("Condition not selected. Select a condition")
            error = True
        num_unaccepted_swaps = list_items.display_unaccepted_swaps(session['user_id'])[0]
        num_unrated_swaps = list_items.display_unrated_swaps(session['user_id'])[0]
        if (num_unaccepted_swaps > 2):
            flash("You have more than 2 unaccepted swaps. Please accept or reject those swaps.")
            error = True
        if (num_unrated_swaps > 5):
            flash("You have more than 5 unrated swaps. Please rate those swaps.")
            error = True

        if error is False:
            try:
                if game_type == 'Jigsaw puzzle':
                    last_id = list_items.insert_item_jigsaw(session['user_id'], title, item_condition, item_description,piece_count)

                elif game_type == 'Computer game':
                    last_id = list_items.insert_item_computer_game(session['user_id'], title, item_condition, item_description, computer_game_platform)
                elif game_type == 'Video game':
                    print((session['user_id'], title, item_condition, item_description, video_game_platform, video_game_media))
                    last_id = list_items.insert_item_video_game(session['user_id'], title, item_condition, item_description, video_game_platform, video_game_media)
                elif game_type == 'Board game':
                    last_id = list_items.insert_board_game(session['user_id'], title, item_condition, item_description)
                elif game_type == 'Card game':
                    last_id = list_items.insert_card_game(session['user_id'], title, item_condition, item_description)

                # Get last item

            except Exception as e:
                error = f"There was an error registering this item."
            else:
                flash("Your item has been listed! Your item number is " + str(last_id) + ".")
        if error is True:
            flash('Your item was not listed.')

    return render_template('forms/listitem.html',
                           game_type_options=game_type_options,
                           video_game_platform_types=video_game_platform_types,
                           video_game_media_types=video_game_media_types,
                           computer_game_platform_types=computer_game_platform_types,
                           condition_types=condition_types)


@bp.route('/myitems', methods=('GET', 'POST'))
def my_items():
    db = get_db()
    cursor = db.cursor(buffered=True)
    myitems = MyItemsForm(cursor)
    inventory_count = myitems.display_inventory_count(session['user_id'])
    inventory_table = myitems.display_inventory_table(session['user_id'])
    return render_template('forms/myitems.html', inventory_count=inventory_count, inventory_table=inventory_table)

@bp.route('/proposeswap', methods=('GET', 'POST'))
def propose_swap():
    """
    form_elements =ProposeSwapForm(cursor)
    target_item = form_elements.get_target_item_name([2])

    item_column_name = target_item[0]
    item_name = target_item[1]
    
    item_column_name=item_column_name,\
        item_name=item_name
    """
    db = get_db()
    cursor = db.cursor(buffered=True)
    invenotry_list = ProposeSwapForm(cursor,db)
    #just need the item title here, and no for loops are need in frontend,/
    #  just passing string as it is

    #parameters from last form/session need to be passed in , which is user selected item_number\
    # and current user's email 
    testing_item_number = '10'
    desired_item_title = invenotry_list.get_target_item_name(testing_item_number)[0][0]
    raw_table = invenotry_list.get_user_own_inventory('ebad@gmail.com')
    
    user_inventory_column_name = raw_table[0]
    user_inventory = raw_table[1]


    if request.method=='POST':
        
        if 'propose_button' in request.form:
            user_selection=request.form['item#']
            print("user_selection is ")
            print(user_selection)
            #need add error messages and comfirmation messages,link back to menu,and pass out user selection
            invenotry_list.insert_new_swap(user_selection,testing_item_number)
            print("swap for ",user_selection," and ",testing_item_number," is successful")
            flash("Selected item has been proposed,please click on the mainmenu link")
   
    #the list of radio buttons need to be inside a form,along with a submit button
    #tried put entire table under form so that the button and radiobuttons are in same form,/
    #but that makes entire table becaome method == post, and jump to if statement
    return render_template('forms/proposeswap.html',user_inventory_column_name=user_inventory_column_name,\
         user_inventory=user_inventory,desired_item_title=desired_item_title   )

@bp.route('/swaphistory', methods=('GET', 'POST'))
def swap_history():
    user_id = session.get('user_id')
    
    db = get_db()
    cursor = db.cursor(buffered=True)
    page_content=SwapHistoryForm(cursor,db)
    form1_raw=page_content.show_current_user_swap_stats(user_id)
    form1_column_name = form1_raw[0]
    form1_element = form1_raw[1]

    form2_raw=page_content.show_current_user_all_swap_history(user_id)
    form2_column_name = form2_raw[0]
    form2_element = form2_raw[1]
    unrated_swap_id = []
    role_list = []
    for i in range(len(form2_element)):
        if form2_element[i][-1] == None and form2_element[i][3]=='accepted':
            item_pro = (form2_element[i][0])
            item_con = (form2_element[i][1])
            role_temp = form2_element[i][4]
            
            swap_id_and_role_conbine = str(item_pro)+'&'+str(item_con)
            unrated_swap_id.append(swap_id_and_role_conbine)
            role_list.append(role_temp)
    print(unrated_swap_id)
    print(role_list)
 


    if request.method == 'POST':
        if 'submit_rating' in request.form:
            for key in request.form:
                for index,item in enumerate(unrated_swap_id):
                    if key == item:
                        selected_rating=request.form[item]
                        selected_swap = item
                        print(index)
                        myrole = role_list[index]
                        splited_swap = selected_swap.split("&")
                        item_pro_query_input = splited_swap[0]
                        item_con_query_input = splited_swap[1]
                        page_content.update_rating(item_pro_query_input,item_con_query_input,selected_rating,myrole)
                        return redirect(url_for('gameswap.swap_history'))
        elif 'detail_link' in request.form:
            selected_swap_id = request.form['detail_link']
            print(selected_swap_id)
            split_swap_detail_link=selected_swap_id.split("&")
            session['pro_item_temp'] = split_swap_detail_link[0]
            session['con_item_temp'] = split_swap_detail_link[1]
            return redirect(url_for('gameswap.swap_details'))

        


    return render_template('forms/swaphistory.html',form1_column_name=form1_column_name,form1_element=form1_element, \
        form2_column_name=form2_column_name,form2_element=form2_element,email=user_id)

@bp.route('/swapdetails', methods=('GET', 'POST'))
def swap_details():
    user_id = session.get('user_id')
    #print(session)
    test_email='chris@gmail.com'
    item_pro=session['pro_item_temp']
    item_con=session['con_item_temp']
    db = get_db()
    cursor = db.cursor(buffered=True)
    page_content=SwapDetailsForm(cursor,db)
    temp_update_form=SwapHistoryForm(cursor,db)
    swap_details_raw=page_content.form1_swapdetails(user_id,item_pro,item_con)
    swap_details_column_name=swap_details_raw[0]
    swap_details_element=swap_details_raw[1]
   
    items_raw=page_content.form34_item_details(item_pro,item_con)

    

    no_none_pro_raw = page_content.remove_none_head_and_elements(items_raw[0],items_raw[1][0])
    item_pro_column_names = no_none_pro_raw[0]
    item_pro_element = no_none_pro_raw[1]

    no_none_con_raw = page_content.remove_none_head_and_elements(items_raw[2],items_raw[3][0])
    item_con_column_names = no_none_con_raw[0]
    item_con_element = no_none_con_raw[1]

    
    
    if swap_details_element[0][3] == 'proposer':
        my_items_number = item_pro_element[0]
    elif swap_details_element[0][3] == 'counterparty':
        my_items_number = item_con_element[0]

    otheruser_raw = page_content.other_user(item_pro,item_con,my_items_number)
    otheruser_column_names = otheruser_raw[0]
    otheruser_column_elements = otheruser_raw[1]

    

    refine_phone_info =[]
    for index,elements in enumerate(otheruser_column_elements[0]):
        if otheruser_column_elements[0][-1] == 0:
            refine_phone_info.append(elements)
            if index > 2:
                break
        else:

            refine_phone_info.append(elements)
            if index > 4:
                refine_phone_info[4] = refine_phone_info[4]+' ('+refine_phone_info[5]+')'
                refine_phone_info.pop()
              
                break
   


    if 'submit_rating_deitals_form' in request.form:
        selected_rating=request.form['user_input_rating']
       # print(selected_rating)
        temp_update_form.update_rating(swap_details_element[0][0],swap_details_element[0][1],selected_rating,swap_details_element[0][-2])
        return redirect(url_for('gameswap.swap_details'))

    return render_template('forms/swapdetails.html',swap_details_column_name=swap_details_column_name,swap_details_element=swap_details_element,\
    item_con_column_names=item_con_column_names,item_con_element=item_con_element,\
    item_pro_column_names=item_pro_column_names,item_pro_element=item_pro_element,\
    otheruser_column_names=otheruser_column_names,otheruser_column_elements=refine_phone_info)