# Imports
import random
import string
import httplib2
import json
import requests

from flask import (Flask,
                   render_template,
                   flash,
                   request,
                   url_for,
                   redirect,
                   jsonify,
                   json,
                   make_response,
                   session as login_session)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSetup import (Base,
                           User,
                           Category,
                           Item)

from oauth2client.client import (flow_from_clientsecrets,
                                 FlowExchangeError)


id_Client = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
app = Flask(__name__)

engine = create_engine(
    'sqlite:///catalogApi.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Db Queries


# add new user
def add_user(login_session):
    user = User(
        userName=login_session['userName'],
        email=login_session['email'],
        img_user=login_session['img_user'])
    session.add(user)
    session.commit()
    return


# check if user in database or add it
def get_user_by_session(login_session):
    try:
        user = session.query(User).filter_by(
         email=login_session['email']).one()
        return user
    except:
        add_user(login_session)
        return session.query(
            User).filter_by(email=login_session['email']).one()


# get one Category By ID
def get_category_by_id(cat_id):
        return session.query(Category).filter_by(id=cat_id).one()


# get All category
def get_all_category():
        return session.query(Category).all()


# get one item by id
def get_one_item_by_id(i_id):
        return session.query(Item).filter_by(id=i_id).join(Category).one()


# get items by Category
def get_items_by_cat(cat_id):
    return session.query(Item).filter_by(category_id=cat_id).all()


# get last 10 items
def get_lasts_items():
    return session.query(Item).order_by(
            Item.id.desc()).limit(10)


# add new row in database or updat
def add_item(item):
    session.add(item)
    session.commit()
    return


# delete row from database
def delete_item(item):
    session.delete(item)
    session.commit()
    return


# --------------------------------------------------------------
# -------------------------API Routes---------------------------
# --------------------------------------------------------------

# get all categories Api JSON
@app.route('/api/catalog/JSON/')
def catalogJSON():
    categories = get_all_category()
    return jsonify(categories=[cat.serialize for cat in categories])


# get Items by category Api JSON
@app.route('/api/catalog/<int:category_id>/items/JSON/')
def itemsJSON(category_id):
    items = get_items_by_cat(category_id)
    return jsonify(items=[item.serialize for item in items])


# get one Item by Category APi JSON
@app.route('/api/catalog/items/<int:item_id>/JSON/')
def itemJSON(item_id):
    item = get_one_item_by_id(item_id)
    return jsonify(item=item.serialize)


# connexion gplus
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # check state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that  token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Tokens user ID does not match user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != id_Client:
        response = make_response(
            json.dumps("Tokens client ID does not match app ."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the  token in the session .
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # get user information email name picture)
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['userName'] = data['name']
    login_session['img_user'] = data['picture']
    login_session['email'] = data['email']

    # check if user in database or add it
    login_session['user_id'] = get_user_by_session(login_session).id
    show_output = ''
    show_output += '<br/>'
    show_output += '<h2>Welcome 😃 '
    show_output += login_session['userName']
    show_output += '!</h2>'
    show_output += '<img src="'
    show_output += login_session['img_user']
    show_output += ' " class="user_img" >'
    show_output += '<br/>'
    return show_output


# user logoff
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    # check status code
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['userName']
        del login_session['email']
        del login_session['img_user']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response



@app.route('/')
@app.route('/catalog/')
def allCategories():
    '''
    show all categories  all the items available
    for that category
    '''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # Call helper methods
    categories = get_all_category()
    latestItems = get_lasts_items()
    return render_template('index.html',
            STATE=state,
            categories=categories,
            items=latestItems,
            user=login_session)




@app.route('/catalog/<int:cat_id>/')
def itemsByCategory(cat_id):
    '''
    choose a one category and shows all the items available
    for that category.
    '''
    # Call helper methods
    categories = get_all_category()
    category = get_category_by_id(cat_id)
    items = get_items_by_cat(cat_id)
    return render_template('category.html',
                           category=category,
                           categories=categories,
                           items=items,
                           user=login_session)


@app.route('/catalog/<int:cat_id>/item/<int:item_id>/')
def getItem(cat_id, item_id):
    '''
    display information about selected item
    '''
    cat = get_category_by_id(cat_id)
    i = get_one_item_by_id(item_id)
    return render_template('item.html',
                           category=cat,
                           item=i,
                           user=login_session)


@app.route('/catalog/<int:cat_id>/addItem', methods=['GET', 'POST'])
def addItemCat(cat_id):
    '''
    create new item
    method GET will open the 'addItem.html' page.
    The method POST insert new item  DB and redirect the user to
    the 'categories.html' page
    '''
    # check if user has been logged in
    if 'userName' not in login_session:
        return redirect(url_for('allCategories'))
    else:
        # call helper method to get Category
        cat = get_category_by_id(cat_id)
        if request.method == 'POST':
            # create new item
            new_item = Item(name=request.form['name'],
                            description=request.form['description'],
                            category_id=cat.id,
                            user_id=login_session['user_id'])
            add_item(new_item)
            return redirect(url_for('itemsByCategory', cat_id=cat.id))

        else:
            return render_template('addItem.html',
                                   cat=cat,
                                   user=login_session)


@app.route('/catalog/<int:cat_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(cat_id, item_id):
    '''
    edit item
    method GET will open the 'editItem.html' page.
    The method POST will update  item  DB and redirect the user to
    the 'item.html' page
    '''
    # check if user has been logged in
    if 'userName' not in login_session:
        return redirect(url_for('allCategories'))
    else:
        categories = get_all_category()
        item = get_one_item_by_id(item_id)
        if request.method == 'POST':
            # user who entered this item is allowed to edit  this item
            if login_session['user_id'] != item.user_id:
                return make_response("""You are not
                 authorized to edit this item.""", 401)
            if request.form['name']:
                item.name = request.form['name']
            if request.form['description']:
                item.description = request.form['description']
            if request.form['Catalog']:
                item.category_id = request.form['Catalog']
            # update that item
            add_item(item)
            return redirect(url_for('getItem',
                            cat_id=item.category_id,
                            item_id=item.id))
        else:
            return render_template('editItem.html',
                                   categories=categories,
                                   item=item,
                                   user=login_session)

# Delete Operations


@app.route('/catalog/<int:cat_id>/delete/<int:item_id>/',
           methods=['GET', 'POST'])
def deleteItem(cat_id, item_id):
    # check if user has been logged in
    if 'userName' not in login_session:
        return make_response("""You are not
        authorized to delete this item.""", 401)
    else:
        categories = get_all_category()
        item = get_one_item_by_id(item_id)
        # user who entered this item is allowed to remove  this item
        if login_session["user_id"] != item.user_id:
                return make_response("""You are not
                 authorized to delete this item.""", 401)
        if request.method == 'POST':
            # delete item
            delete_item(item)
            return redirect(url_for('allCategories'))
        else:
            return render_template('deleteItem.html',
                                   categories=categories,
                                   item=item,
                                   user=login_session)
if __name__ == "__main__":
    app.secret_key = "your_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
