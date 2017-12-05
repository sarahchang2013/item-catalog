from flask import Flask, render_template
from flask import request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
import random, string
from flask import session as login_session

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def login():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)


@app.route('/')
@app.route('/index')
def homePage():
	categories = session.query(Category).all()
	latestItems = session.query(Item).order_by(Item.id.desc()).limit(10)
	return render_template("index.html", 
							categories=categories, 
							latestItems=latestItems)


@app.route('/catalog/<name>/items')
def categoryDetails(name):
	categories = session.query(Category).all()
	category = session.query(Category).filter(Category.name == name).one()
	items = category.items
	count = len(items)
	return render_template("categoryDetails.html", 
							categories=categories, 
							category_name=name, 
							items=items, count=count)


@app.route('/catalog/<category_name>/<item_title>')
def itemDescription(category_name, item_title):
	item = session.query(Item).filter(and_(Item.title == item_title, Item.category.has(Category.name == category_name))).one()
	return render_template("itemDescription.html", category_name=category_name, item=item)


@app.route('/catalog.json')
def catalogJSON():
	categories = session.query(Category).all()
	return jsonify(Category=[c.serialize for c in categories])


@app.route('/catalog/add', methods=['GET','POST'])
def addItem():
	if request.method == 'POST':
		#Retrieve form data
		title = request.form['title']
		description = request.form['description']
		category_id = request.form['category']
		existing_items = session.query(Item).filter(and_(Item.title == title, Item.category_id == category_id)).all()
		if len(existing_items):
			flash('Item already exists!')
			return redirect('/index')
		else:
			newItem = Item(title=title, 
							description=description, 
							category_id=category_id)
			session.add(newItem)
			session.commit()
			return redirect('/index')
	else:
		return render_template("addItem.html")


@app.route('/catalog/<category_name>/<item_title>/edit', methods=['GET','POST'])
def editItem(category_name, item_title):
	if request.method == 'POST':
		#Retrieve form data
		title = request.form['title']
		description = request.form['description']
		category_id = request.form['category']
		existing_items = session.query(Item).filter(and_(Item.title == title, Item.category_id == category_id)).all()
		if len(existing_items) >= 1:
			flash('Item already exists, please pick a different title or category.')
			return render_template("editItem.html", item_title=item_title)
		else:
			editedItem = session.query(Item).filter(and_(Item.title == item_title, Item.category.has(Category.name == category_name))).one()
			editedItem.title = title
			editedItem.description = description
			editedItem.category_id = category_id
			new_cat_name = editedItem.category.name
			session.commit()
			return redirect('/catalog/{}/{}'.format(new_cat_name, editedItem.title))
	else:
		return render_template("editItem.html")


@app.route('/catalog/<category_name>/<item_title>/delete', methods=['GET','POST'])
def deleteItem(category_name, item_title):
	if request.method == 'POST':
		deletedItem = session.query(Item).filter(and_(Item.title == item_title, Item.category.has(Category.name == category_name))).first()
		session.delete(deletedItem)
		session.commit()
		flash('Item deleted!')
		return redirect('/index')
	else:
		return render_template("deleteItem.html", category_name=category_name, item_title=item_title)


if __name__ == '__main__':
	app.debug = True
	app.secret_key = 'super_secret_key'
	app.run(host='0.0.0.0', port=8000)