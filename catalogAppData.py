from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from databaseSetup import Base, User, Category, Item

engine = create_engine('sqlite:///catalogApi.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# add 2 users
user1 = User(userName="anex", email="anex@bm.com")
session.add(user1)
session.commit()

print("added user 1!")

user2 = User(userName="amine", email="amine@bm.com")
session.add(user2)
session.commit()

print("added user 2!")

# Category 1
category1 = Category(name="Soccer", user_id=1)

session.add(category1)
session.commit()

# Category 2
category2 = Category(name="Basketball", user_id=1)

session.add(category2)
session.commit()

# Category 3
category3 = Category(name="Baseball", user_id=1)

session.add(category3)
session.commit()

# Category 4
category4 = Category(name="Frisbee", user_id=1)

session.add(category4)
session.commit()

# Category 5
category5 = Category(name="Snowboarding", user_id=1)

session.add(category5)
session.commit()

# Category 6
category6 = Category(name="Rock Climbing", user_id=1)

session.add(category6)
session.commit()

# Category 7
category7 = Category(name="Football", user_id=1)

session.add(category7)
session.commit()

# Category 8
category8 = Category(name="Skating", user_id=1)

session.add(category8)
session.commit()

# Category 9
category9 = Category(name="Hockey", user_id=1)

session.add(category9)
session.commit()

print("added categories!")

# Item 1
item1 = Item(
    name="item 1",
    description="description item 1", category_id=5, user_id=1)
session.add(item1)
session.commit()

# Item 2
item2 = Item(
    name="item 2",
    description="description item 2", category_id=1, user_id=1)
session.add(item2)
session.commit()

# Item 3
item3 = Item(
    name="item 3",
    description="description item 3", category_id=1, user_id=1)
session.add(item3)
session.commit()

# Item 4
item4 = Item(
    name="item 4",
    description="description item 4", category_id=3, user_id=1)
session.add(item4)
session.commit()

# Item 5
item5 = Item(
    name="item 5",
    description="description item 4", category_id=4, user_id=1)
session.add(item5)
session.commit()

# Item 6
item6 = Item(
    name="item 5",
    description="description item 5", category_id=1, user_id=1)
session.add(item6)
session.commit()

# Item 7
item7 = Item(
    name="item 6",
    description="description item 6", category_id=1, user_id=1)
session.add(item7)
session.commit()

# Item 8
item8 = Item(
    name="item 7",
    description="item 7 description", category_id=5, user_id=1)
session.add(item8)
session.commit()

# Item 9
item9 = Item(
    name="item 8",
    description="item 8 descriptio", category_id=5, user_id=1)
session.add(item9)
session.commit()

# Item 10
item10 = Item(
    name="item 9",
    description="item 9 description", category_id=9, user_id=1)
session.add(item10)
session.commit()

print("added items!")
