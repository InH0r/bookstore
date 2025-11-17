
import os
import sys
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, VARCHAR, create_engine, Date, Boolean, Float, TIMESTAMP,  ForeignKey
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from bookstore.model.base import Base


class Genre(Base):
    __tablename__ = 'd_genre'
    genre_id = Column(Integer, primary_key=True, autoincrement=True)
    genre = Column(VARCHAR(50))
    products = relationship('Shops', back_populates='genre',  cascade="all, save-update")


class Shops(Base):
    __tablename__ = 'f_product'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(500))
    rating = Column(VARCHAR(50))
    upc = Column(VARCHAR(300))
    product_type = Column(VARCHAR(50))
    genre_id = Column(Integer, ForeignKey('d_genre.genre_id'))
    genre = relationship('Genre', back_populates='products')
    prices = relationship('Price', back_populates='product', cascade="all, save-update")


class Price(Base):
    __tablename__ = 'd_price'

    price_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('f_product.product_id'))
    price_excl_tax = Column(Float)
    price_incl_tax = Column(Float)
    tax = Column(Float)
    product = relationship('Shops', back_populates='prices')
