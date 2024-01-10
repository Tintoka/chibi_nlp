import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *






class Base(DeclarativeBase):
    pass

engine = sqlalchemy.create_engine("sqlite+pysqlite:////home/tohidkhaah/DataBase/chibi_nlp.db", echo=True)
s = Session(engine)




class APIKeys(Base):
    __tablename__="api_keys"  

    id: Mapped[str] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(nullable=True)
    isAvailable: Mapped[bool]  = mapped_column(nullable=False)


    def __repr__(self) -> str:
         return f"APIKeys(id={self.id!r}, name={self.name!r},isAvailable={self.isAvailable!r})"
    


# Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)





# setAPIAvailability(s, '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', False)
# print(getAvailableAPIKey(s))