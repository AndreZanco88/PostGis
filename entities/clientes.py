from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, text, DateTime
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, sessionmaker
from config.dbconfig import Base

class Clientes(Base):
    __tablename__ = 'clientes'

    id = Column('ID', Integer, primary_key = True, autoincrement = True)
    cliente = Column('cliente', String)

    def __repr__(self):
        return f"Cliente [nome={self.cliente}, id={self.id}]"