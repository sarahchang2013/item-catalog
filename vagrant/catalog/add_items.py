from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# add a dummy user
user1 = User(name="dummyUser", email="dummyuseremail")
session.add(user1)
session.commit()

# add new categories
cat1 = Category(name="Soccer")
session.add(cat1)
session.commit()

cat2 = Category(name="Basketball")
session.add(cat2)
session.commit()

cat3 = Category(name="Baseball")
session.add(cat3)
session.commit()

cat4 = Category(name="Frisbee")
session.add(cat4)
session.commit()

cat5 = Category(name="Snowboarding")
session.add(cat5)
session.commit()

cat6 = Category(name="Rock Climbing")
session.add(cat6)
session.commit()

cat7 = Category(name="Skating")
session.add(cat7)
session.commit()

cat8 = Category(name="Hockey")
session.add(cat8)
session.commit()


# add new items in each category
item1 = Item(user_id=1, category_id=1, title="Soccer Cleats",
             description="The Shoes")
session.add(item1)
session.commit()

item2 = Item(user_id=1, category_id=1, title="Jersey", description="The Shirt")
session.add(item2)
session.commit()

item3 = Item(user_id=1, category_id=3, title="Bat", description="The bat")
session.add(item3)
session.commit()

item4 = Item(user_id=1, category_id=5, title="Snowboard",
             description="The Snowboard")
session.add(item4)
session.commit()
