from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Item, User

engine = create_engine('sqlite:///Catalog.db')
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

# Create dummy user
User1 = User(name="admin", email="alberto.rivera@gmail.com")
session.add(User1)
session.commit()

# Dummy books data
book1 = Item(
    id = 1
    name= "Rese&ntilde;a: The Last Jedi",
            coverUrl="""https://books.google.com/books/content/
               images/frontcover/F9uIBAAAQBAJ?fife=w300-rw""",
               description="hello", category="Romance", user_id=1)

session.add(book1)
session.commit()



print "added Items!"
