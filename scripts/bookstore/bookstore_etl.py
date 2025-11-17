import os
import sys
from time import sleep
import requests
import datetime as datetime
from sqlalchemy import Column, Float, Integer, VARCHAR, create_engine, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from bookstore.model.base import Base
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from bookstore.model.books_sh import  Shops
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from bookstore.model.books_sh import  Genre
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from bookstore.model.books_sh import  Price
from airflow.decorators import task
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from bookstore.parse_books import get_info
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

engine = create_engine(SQLALCHEMY_DATABASE_URI) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session_local = SessionLocal()
#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
def check_etl():
    books_data = list(get_info())

    for  item in books_data:
        normalized = {k.lower().replace(' ', '_'): v for k, v in item.items()}
        key_map = {
            'price_(excl._tax)': 'price_excl_tax',
            'price_(incl._tax)': 'price_incl_tax',
        }
        mapped = {}
        for k, v in normalized.items():
            new_key = key_map.get(k, k) 
            mapped[new_key] = v
        
        ggenre = Genre(
            genre=mapped["genre"],
        )
        
        product = Shops(
        
            title=mapped["title"],
            rating=mapped["rating"],
            upc=mapped.get("upc"),
            product_type=mapped.get("product_type"),
            genre = ggenre
        
        )
       
        pr = Price(
            price_excl_tax=float(mapped.get("price_excl_tax", 0)),
            price_incl_tax=float(mapped.get("price_incl_tax", 0)),
            tax=float(mapped.get("tax", 0)),
            product = product
        )
    
        session_local.add(product)
        session_local.commit()
    return 'finished'
  