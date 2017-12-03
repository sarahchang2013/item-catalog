from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User


app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/catalog.json')
def catalogJSON():
	categories = session.query(Category).all()
	return jsonify(Category=[c.serialize for c in categories])


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=9000)