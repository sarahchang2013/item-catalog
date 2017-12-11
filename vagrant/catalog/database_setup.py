from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
	__tablename__ = 'user'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250))


class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	items = relationship("Item", back_populates="category")

	#serialize function
	@property
	def serialize(self):
		"""Return object data in serialization"""
		if len(self.items):
			return {
					"Item": [i.serialize for i in self.items],
					"name": self.name,
					"id": self.id
					}
		else:
			return {
					"name": self.name,
					"id": self.id
					}


class Item(Base):
	__tablename__ = 'item'

	id = Column(Integer, primary_key=True)
	title = Column(String(250), nullable=False)
	description = Column(String(800), nullable=False)
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship("Category", back_populates="items")
	user_id = Column(Integer, ForeignKey('user.id'))	

	#serialize function
	@property
	def serialize(self):
		"""Return object data in serialization"""
		return {
				"cat_id": self.category_id,
				"description": self.description,
				"id": self.id,
				"title": self.title
				}


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
