from flask import Flask, render_template
from flask import request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
import random, string
from flask import session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
from flask import make_response

app = Flask(__name__)

#Prepare for database query
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()


#Login page
@app.route('/login')
def login():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	session['state'] = state
	return render_template('login.html', STATE=state)


#Connect to Google account
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != session['state']:
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
    CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(session)
    session['user_id'] = user_id

    session['logged_in'] = True
    output = ''
    output += '<h1>Welcome, '
    output += session['username']
    output += '!</h1>'
    output += '<img src="'
    output += session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % session['username'])
    print "done!"
    return output

# User Helper Functions
def createUser(session):
    newUser = User(name=session['username'], email=session[
                   'email'], picture=session['picture'])
    dbsession.add(newUser)
    dbsession.commit()
    user = dbsession.query(User).filter_by(email=session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = dbsession.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = dbsession.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


#Disconnect from Google account. 
#If new third party is added, seperate '/logout' to a new function,  
#and render a new page for logout options.
@app.route('/logout')
@app.route('/gdisconnect')
def logout():
	# Only disconnect a connected user.
	access_token = session.get('access_token')
	if access_token is None:
		response = make_response(
			json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	if result['status'] == '200':
		del session['access_token']
		del session['gplus_id']
		del session['username']
		del session['email']
		del session['picture']
		session.pop('logged_in', None)
		flash('You are now logged out.')
		return redirect('/index')
	else:
		response = make_response(json.dumps('Failed to revoke token for given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response


#Index page
@app.route('/')
@app.route('/index')
def homePage():
	categories = dbsession.query(Category).all()
	latestItems = dbsession.query(Item).order_by(Item.id.desc()).limit(10)
	return render_template("index.html", 
							categories=categories, 
							latestItems=latestItems)


#Show items in a category
@app.route('/catalog/<name>/items')
def categoryDetails(name):
	categories = dbsession.query(Category).all()
	category = dbsession.query(Category).filter(Category.name == name).one()
	items = category.items
	count = len(items)
	return render_template("categoryDetails.html", 
							categories=categories, 
							category_name=name, 
							items=items, count=count)


#Show description of an item in a category
@app.route('/catalog/<category_name>/<item_title>')
def itemDescription(category_name, item_title):
	item = dbsession.query(Item).filter(and_(Item.title == item_title, Item.category.has(Category.name == category_name))).one()
	return render_template("itemDescription.html", category_name=category_name, item=item)


#JSON endpoint to show all items in each category
@app.route('/catalog.json')
def catalogJSON():
	categories = dbsession.query(Category).all()
	return jsonify(Category=[c.serialize for c in categories])


#Page for adding new items
@app.route('/catalog/add', methods=['GET', 'POST'])
def addItem():
	if 'username' not in session:
		return redirect('/login')
	if request.method == 'POST':
		#Retrieve form data
		title = request.form['title']
		description = request.form['description']
		category_id = request.form['category']
		#Check if an item with the same title and category already exists
		existing_items = dbsession.query(Item).filter(and_(Item.title == title, Item.category_id == category_id)).all()
		if len(existing_items):
			flash('Item already exists!')
			return redirect('/index')
		else:
			#New item confirmed, add to database
			newItem = Item(title=title, 
							description=description, 
							category_id=category_id)
			dbsession.add(newItem)
			dbsession.commit()
			return redirect('/index')
	else:
		return render_template("addItem.html")


#Page for editting an item in a category
@app.route('/catalog/<category_name>/<item_title>/edit', methods=['GET','POST'])
def editItem(category_name, item_title):
	if 'username' not in session:
		return redirect('/login')
	#Check if current user's id is the same as item.user_id
	currentItem = dbsession.query(Item).filter(and_(Item.title == item_title, Item.category.name == category_name)).one()
	if currentItem.user_id != session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to edit this item. Please create your own item in order to edit.');}</script><body onload='myFunction()'>"
	if request.method == 'POST':		
		#Retrieve form data
		title = request.form['title']
		description = request.form['description']
		category_id = request.form['category']
		#Check if an item with the same title and category already exists
		existing_items = dbsession.query(Item).filter(and_(Item.title == title, Item.category_id == category_id)).all()
		if len(existing_items) >= 1:
			flash('Item already exists, please pick a different title or category.')
			return render_template("editItem.html", category_name=category_name, item_title=item_title)
		else:
			#No existing item with same title and category, update it
			editedItem = dbsession.query(Item).filter(and_(Item.title == item_title, Item.category.has(Category.name == category_name))).one()
			editedItem.title = title
			editedItem.description = description
			editedItem.category_id = category_id
			new_cat_name = editedItem.category.name
			dbsession.commit()
			return redirect('/catalog/{}/{}'.format(new_cat_name, editedItem.title))
	else:
		return render_template("editItem.html", category_name=category_name, item_title=item_title)


#Page for deleting an item in a category
@app.route('/catalog/<category_name>/<item_title>/delete', methods=['GET','POST'])
def deleteItem(category_name, item_title):
	if 'username' not in session:
		return redirect('/login')
	currentItem = dbsession.query(Item).filter(and_(Item.title == item_title, Item.category.name == category_name)).one()
	if currentItem.user_id != session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to edit this item. Please create your own item in order to edit.');}</script><body onload='myFunction()'>"
	if request.method == 'POST':
		#In case there are two identical items, use first() to at least delete one.
		#Avoid error when using one()
		deletedItem = dbsession.query(Item).filter(and_(Item.title == item_title, Item.category.has(Category.name == category_name))).first()
		dbsession.delete(deletedItem)
		dbsession.commit()
		flash('Item deleted!')
		return redirect('/index')
	else:
		return render_template("deleteItem.html", category_name=category_name, item_title=item_title)


if __name__ == '__main__':
	app.debug = True
	app.secret_key = 'super_secret_key'
	#Open "http://localhost:8000" in browser to avoid origin error in OAuth
	#Google API console should use "http://localhost:8000"
	#The console doesn't support 0.0.0.0
	app.run(host='0.0.0.0', port=8000)