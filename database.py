import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
import sqlalchemy_utils as su
from sqlalchemy.exc import OperationalError

import os







class Base(DeclarativeBase):
    pass

metadata = MetaData()
current_directory = os.getcwd()

#check if database exists, if not, create one.
path = current_directory + "/DataBase"

class APIKeys(Base):
    __tablename__="api_keys"  

    id: Mapped[str] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(nullable=True)
    isAvailable: Mapped[bool]  = mapped_column(nullable=False)


    def __repr__(self) -> str:
         return f"APIKeys(id={self.id!r}, name={self.name!r},isAvailable={self.isAvailable!r})"

engine = sqlalchemy.create_engine("sqlite+pysqlite:///" + path + "/chibi_nlp.db", echo=True)
# Reflect the database
metadata.reflect(bind=engine)

# Check if the table existsyaml


# Base.metadata.drop_all(engine)
# print("Droped the database!")
        
if(os.path.exists(path)):
    # print(su.database_exists("sqlite+pysqlite:///" + path + "/chibi_nlp.db"))
    engine = sqlalchemy.create_engine("sqlite+pysqlite:///" + path + "/chibi_nlp.db", echo=True)
    try:
        engine.connect()
        if 'api_keys' in metadata.tables:
            print("Table exists")
        else:
            print("Table does not exist")
            Base.metadata.create_all(engine)
            print("Created the table")
        print(su.database_exists("sqlite+pysqlite:///" + path + "/chibi_nlp.db"))
    except OperationalError:    
        Base.metadata.create_all(engine)
        print("Created the Database!")       
else:
    os.makedirs(path)
    print("Created the Database Folder!") 
    engine = sqlalchemy.create_engine("sqlite+pysqlite:///" + path + "/chibi_nlp.db", echo=True)
    Base.metadata.create_all(engine)
    print("Created the Database!") 



s = Session(engine)












