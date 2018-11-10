from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

from flask import session as login_session

import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# validating current loggedin user
def check_user():
    if login_session:
        try:
            email = login_session['email']
            return session.query(User).filter_by(email=email).one_or_none()
        except:
            return None
    else:
        None

# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None



# Create anti-forgery state token
@app.route('/login')
def showLogin():
    print("****WELCOME TO THE LOGGIN PAGE******")
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/category/<int:category_id>/menu/JSON')
def categoryMenuJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/category/<int:category_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(category_id, menu_id):
    Menu_Item = session.query(Item).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/category/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


# Show all categories
@app.route('/')
@app.route('/category/')
@app.route('/catalog/')
@app.route('/catalog')
def showCategories():
    print("!\n!\n!")
    #print(login_session['email'])
    print(check_user())
    categories = session.query(Category).all()
    for categorie in categories:
        print("categorie.id: " + str(categorie.id))
        print("categorie.name: " + str(categorie.name))
        print("categorie.user_id: " + str(categorie.user_id))
    # return "This page will show all my categories"
    print("This is the result of check_user(): " + str(check_user()))
    user = check_user()
    #print(user.email)
    return render_template('catalog.html', categories=categories, user=check_user())

def showNavbar():
    categories = session.query(Category).all()
    return render_template('navbar.html', categories=categories)



# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'], 
            picture_url=request.form['picture_url'],
            user_id=check_user().id)
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')
    # return "This page will be for making a new category"

# Edit a category


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            return redirect(url_for('showCategories'))
    else:
        return render_template(
            'editCategory.html', category=editedCategory)

    # return 'This page will be for editing category %s' % category_id

# Delete a category


@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(
            url_for('showCategories', category_id=category_id))
    else:
        return render_template(
            'deleteCategory.html', category=categoryToDelete)
    # return 'This page will be for deleting category %s' % category_id


# Show a category menu
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/menu/')
def showItems(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    #items = session.query(Item).filter_by(category_id = category_id).all()

    items = session.query(Item).filter_by(category_id=category_id).order_by(Item.id.desc())
    #items = session.query(Item).order_by(Item.id.desc())
    return render_template('menu.html', items=items, category=category, categories=categories, user = check_user())
    # return 'This page is the menu for category %s' % category_id

# Create a new menu item


@app.route(
    '/category/<int:category_id>/menu/new/', methods=['GET', 'POST'])
def newItem(category_id):
    """return "This page will be for making a new catalog item" """
    categories = session.query(Category).all()
    if request.method == 'POST':
        #return redirect(url_for('showCategories'))
        newItem = Item(
            name=request.form['name'], 
            description=request.form['description'], 
            price=request.form['price'], 
            picture_url=request.form['picture_url'], 
            category_id=category_id )#, user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        #flash("New catalog item created!", 'success')
        print("New catalog item created!")

        #newCategory = Category(name=request.form['name'])
        #session.add(newCategory)
        #session.commit()
        #return redirect(url_for('showCategories'))

        return redirect(url_for('showCategories'))
    else:
        category = session.query(Category).filter_by(id=category_id).one()
        return render_template('newitem.html', category=category, categories=categories)


# Edit a menu item


@app.route('/category/<int:category_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, menu_id):
    editedItem = session.query(Item).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:

        return render_template(
            'edititem.html', category_id=category_id, menu_id=menu_id, item=editedItem)

    # return 'This page is for editing menu item %s' % menu_id

# Delete a menu item


@app.route('/category/<int:category_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_id, menu_id):
    itemToDelete = session.query(Item).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteitem.html', item=itemToDelete)
    # return "This page is for deleting menu item %s" % menu_id



# google signin function

@app.route('/gconnect', methods=['POST'])
def gConnect():
    if request.args.get('state') != login_session['state']:
        response.make_response(json.dumps('Invalid State paramenter'),
                               401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code

    code = request.data
    try:

        # Upgrade the authorization code into a credentials object

        oauth_flow = flow_from_clientsecrets('client_secrets.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps("""Failed to upgrade the
        authorisation code"""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    header = httplib2.Http()
    result = json.loads(header.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
                            """Token's user ID does not
                            match given user ID."""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            """Token's client ID
            does not match app's."""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already connected.'),
                          200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['credentials'] = access_token
    login_session['id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # ADD PROVIDER TO LOGIN SESSION
    print(data)
    login_session['name'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'
    login_session['username'] = data['email']
    login_session['credentials'] = access_token
    #login_session['gplus_id'] = data['gplus_id']
    if not check_user():
        createUser(login_session)

    return jsonify(
        name = login_session['name'],
        picture = login_session['picture'],
        email = login_session['email'],
        provider = login_session['provider'],
        username = login_session['username'],
        credentials = login_session['credentials'])


# logout user

@app.route('/logout', methods=['post'])
def logout():

    # Disconnect based on provider

    if login_session.get('provider') == 'google':
        return gdisconnect()
    else:
        response = make_response(json.dumps({'state': 'notConnected'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:

            #del login_session['gplus_id']
        del login_session['credentials']

        #del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['id']
        del login_session['provider']
        del login_session['username']
        del login_session['name']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))

if __name__ == '__main__':
    app.secret_key = 'password'
    #app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run(host='0.0.0.0', port=5010)