#===================
# Imports
#===================

import random
import string
import httplib2
import json
import requests

#===================
# Flask imports
#===================
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import make_response, flash
from database_setup import Base, User, Category, Item
from flask import session as login_session

#===================
# sqlalchemy imports
#===================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#=================================
# imports from database_setup file
#=================================
from database_setup import Base, User, Category, Item

#===================
# oauth imports
#===================
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

#===================
# Flask instance
#===================
app = Flask(__name__)

#===================
# GConnect CLIENT_ID
#===================

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "catalog"

#================================================
# Connect to Database and create database session
#================================================

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#===================
# Login Routing
#===================

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Connect OAuTH with Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected'
                                            ), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: '
    output += '150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("Welcome %s" % login_session['username'])
    print login_session
    return output


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


# Logout Google OAuTH
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print result
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        # logout
        response = redirect(url_for('homePage'))
        flash("You are now logged out.")
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


#===================
# Flask Routing
#===================

# Home page
@app.route('/')
def homePage():
    categories = session.query(Category).order_by(Category.name.asc())
    items = session.query(Item).order_by(Item.category_id.desc())
    credentials = login_session.get('credentials')
    if credentials is None:
        return render_template('category.html', categories=categories,
                               items=items)
    else:
        return render_template('category.html', categories=categories,
                               items=items, login_session=login_session)


# Show all items that belong to a category
@app.route('/category/<int:category_id>/items')
def showCategoryItems(category_id):
    credentials = login_session.get('credentials')
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()

    if credentials is None:
        return render_template('categoryItems.html', items=items,
                               categories=categories, category=category)
    else:
        return render_template('categoryItems.html', items=items,
                               categories=categories, category=category,
                               login_session=login_session)

# Show a description of a category item
@app.route('/category/<int:category_id>/item/<int:item_id>')
def categoryItem(category_id, item_id):
    credentials = login_session.get('credentials')
    item = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if credentials is None:
        return render_template('itemDescription.html', item=item,
                               category=category)
    else:
        return render_template('itemDescription.html', item=item,
                               category=category, login_session=login_session)


# Add a category item
@app.route('/category/new', methods=['GET', 'POST'])
def newItem():
    credentials = login_session.get('credentials')
    if credentials is None:
        return redirect('/')
    category_list = session.query(Category).all()
    if request.method == 'POST':
        selectedCategory = name = request.form['category']
        category = session.query(Category).filter_by(id=selectedCategory).one()
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       category=category, user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('%s item successfully added!' % newItem.name)
        return redirect(url_for('homePage'))
    else:
        return render_template('addItem.html',
                               category_list=category_list,
                               login_session=login_session)


# Edit category item
@app.route('/category/<int:category_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    credentials = login_session.get('credentials')
    if credentials is None:
        return redirect('/')
    categories = session.query(Category).all()
    editedItem = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if login_session['user_id'] != editedItem.user_id:
        flash('You are not authorized to edit %s item created by another user'
              '!' % editedItem.name)
        return redirect(url_for('homePage'))
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category_id = request.form['category']
        session.add(editedItem)
        session.commit()
        flash('Item updated!')
        return redirect(url_for('homePage'))
    else:
        return render_template(
            'editItem.html', item=editedItem,
            categories=categories, category=category,
            login_session=login_session)


# Delete category item
@app.route('/category/<int:category_id>/item/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    credentials = login_session.get('credentials')
    if credentials is None:
        return redirect('/')
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if login_session['user_id'] != itemToDelete.user_id:
        flash('You are not authorized to delete %s '
              'item created by another user'
              '!' % itemToDelete.name)
        return redirect(url_for('homePage'))
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item deleted!')
        return redirect(
            url_for('showCategoryItems', category_id=category.id))
    else:
        return render_template(
            'deleteItem.html', item=itemToDelete,
            category=category, login_session=login_session)


#===================
# JSON
#===================

# JSON APIs to view Catagory and Item Information
@app.route('/catalog/categories/JSON')
def allCategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])


@app.route('/catalog/items/JSON')
def allItemsJSON():
    items = session.query(Item).all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/catalog/<int:category_id>/items/JSON')
def categoryItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/catalog/<int:category_id>/items/<int:item_id>/JSON')
def categoryItemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
