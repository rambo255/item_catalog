#===================
# sqlalchemy imports
#===================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#=================================
# imports from database_setup file
#=================================
from database_setup import Base, User, Category, Item


engine = create_engine('sqlite:///catalog.db')
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

# Delete Categories if exisitng.
session.query(Category).delete()
# Delete Items if exisitng.
session.query(Item).delete()
# Delete Users if exisitng.
session.query(User).delete()

# Create dummy user
User1 = User(name="Rambo255", email="kirtivardhan.rai@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


# Category Items for Catalog App data

# Soccer Category dummy App Data
Cricket = Category(name="Cricket")

session.add(Cricket)
session.commit()

Cricket_item1 = Item(
    name=" Ball",
    description="""An leather ball used in playing Cricket""",
    category=Cricket)

session.add(Cricket_item1)
session.commit()

Cricket_item2 = Item(
    name=" Bat",
    description="""An wooden bat is used in playing Cricket""",
    category=Cricket)

session.add(Cricket_item2)
session.commit()


# Basketball Category App Data

basketball = Category(name="Basketball")

session.add(basketball)
session.commit()

basketball_item1 = Item(
    name="Basketball",
    description="""A basketball is a spherical inflated ball used in basketball games. Basketballs typically range in 
                size from very small promotional items only a few inches in diameter to extra large balls nearly a foot
                in diameter used in training exercises. """,
    category=basketball)

session.add(basketball_item1)
session.commit()

# Hockey Category App Data
hockey = Category(name="Hockey")

session.add(hockey)
session.commit()

hockey_item1 = Item(
    name="Stick",
    description="""Hockey stick is a long, thin implement with a curved end, used to hit or direct the puck or ball in 
    ice hockey or field hockey.""",
    category=hockey)

session.add(hockey_item1)
session.commit()

hockey_item2 = Item(
    name="Puck",
    description="""Puck is a black disk made of hard rubber, the focus of play in ice hockey. """,
    category=hockey)

session.add(hockey_item2)
session.commit()


# Frisbee Category App Data
frisbee = Category(name="Frisbee")

session.add(frisbee)
session.commit()

frisbee_item1 = Item(
    name="Flying Disc",
    description="""Flying disc (also called frisbee) is a gliding toy or sporting item that is generally plastic and 
                roughly 20 to 25 centimetres (8 to 10 in) in diameter with a lip, used recreationally and competitively 
                for throwing and catching, for example, in flying disc games.""",
    category=frisbee)

session.add(frisbee_item1)
session.commit()

# Snowboarding Category App Data
snowboarding = Category(name="Snowboarding")

session.add(snowboarding)
session.commit()

snowboarding_item1 = Item(
    name="Snowboard",
    description="""Snowboard is a board resembling a short, broad ski, used for sliding downhill on snow""",
    category=snowboarding)

session.add(snowboarding_item1)
session.commit()

snowboarding_item2 = Item(
    name="Ski Boots",
    description="""Ski boots are footwear used in skiing to provide a way to attach the skier to skis using ski 
                    bindings. The ski/boot/binding combination is used to effectively transmit control inputs from the 
                    skier's legs to the snow.""",
    category=snowboarding)

session.add(snowboarding_item2)
session.commit()


# Rockclimbing Category App Data
rockclimbing = Category(name="Rock Climbing")

session.add(rockclimbing)
session.commit()

rockclimbing_item1 = Item(
    name="Rope",
    description="""A dynamic rope is a specially constructed, somewhat elastic rope used primarily in rock climbing, 
                ice climbing, and mountaineering. This 'stretch' is what makes it 'dynamic', in contrast to a static 
                rope that has very low elongation under load.""",
    category=rockclimbing)

session.add(rockclimbing_item1)
session.commit()

rockclimbing_item2 = Item(
    name="Carabiner",
    description="""A carabiner is a specialized type of shackle, a metal loop with a spring-loaded gate used to quickly 
                and reversibly connect components, most notably in safety-critical systems. """,
    category=rockclimbing)

session.add(rockclimbing_item2)
session.commit()

# Foosball Category App Data
foosball = Category(name="Foosball")

session.add(foosball)
session.commit()

foosball_item1 = Item(
    name="Foosball table",
    description="""A table game resembling soccer in which the ball is moved by manipulating rods to which 
                small figures of players are attached""",
    category=foosball)

session.add(foosball_item1)
session.commit()

foosball_item2 = Item(
    name="Foosball",
    description="""A small ball designed to play with Foosball""",
    category=foosball)

session.add(foosball_item2)
session.commit()

# Rabbi Category App Data
Rabbi = Category(name="Rabbi")

session.add(Rabbi)
session.commit()

Rabbi_item1 = Item(
    name="Rabbi Ball",
    description="""A long oval shaped ball which is used to play Rabbi""",          
    category=Rabbi)

session.add(Rabbi_item1)
session.commit()

print "Added initial data"
