import sys

import os
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    userName = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    img_user = Column(String)

    @property
    def serialize(self):
        """ Return object data in easily serializeable format """
        return {
           "userName": self.userName,
           "id": self.id,
           "email": self.email,
        }


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)

    @property
    def serialize(self):
        """ Return object data in easily serializeable format """
        return {
            "name": self.name,
            "id": self.id
        }


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)

    @property
    def serialize(self):
        """ Return object data in easily serializeable format """
        return {
            "name": self.name,
            "description": self.description
        }

engine = create_engine(
    'sqlite:///catalogApi.db', connect_args={'check_same_thread': False})

Base.metadata.create_all(engine)
print('created Db')
