from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User


app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/index')
def homePage():
	categories = session.query(Category).all()
	latestItems = session.query(Item).order_by(Item.id.desc()).limit(10)
	return render_template("index.html", categories=categories, latestItems=latestItems)


@app.route('/catalog/<name>/items')
def categoryDetails(name):
	categories = session.query(Category).all()
	category = session.query(Category).filter(Category.name == name).one()
	items = category.items
	count = len(items)
	return render_template("categoryDetails.html", categories=categories, category_name=name, items=items, count=count)


@app.route('/catalog/<category_name>/<item_title>')
def itemDescription(category_name, item_title):
	item = session.query(Item).filter(Item.title == item_title).one()
	return render_template("itemDescription.html", item=item)


@app.route('/catalog.json')
def catalogJSON():
	categories = session.query(Category).all()
	return jsonify(Category=[c.serialize for c in categories])


@app.route('/catalog/add', methods=['GET','POST'])
def addItem():
	if request.method == 'POST':
		#Retrieve form data
		#code here
		newItem = Item(title=title, description=description, category_id=category_id, user_id=user_id)
		session.add(newItem)
		session.commit()
		return render_template("index.html")
	else:
		return render_template("addItem.html")


@app.route('/catalog/<item_title>/edit', methods=['GET','POST'])
def editItem(item_title):
	if request.method == 'POST':
		editedItem = session.query(Item).filter(Item.title == item_title).one()
		#Retrieve form data
		#code here
		editedItem.title = title
		editedItem.description = description
		editedItem.category_id = category_id
		session.commit()
		return render_template("itemDescription.html", item=item)
	else:
		return render_template("editItem.html", item_title=item_title)


@app.route('/catalog/<item_title>/delete', methods=['GET','POST'])
def deleteItem(item_title):
	if request.method == 'POST':
		deletedItem = session.query(Item).filter(Item.title == item_title).one()
		#Retrieve form data
		#code here
		session.delete(deletedItem)
		session.commit()
		return render_template("index.html")
	else:
		return render_template("deleteItem.html", item_title=item_title)


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=8000)