from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, text, DateTime
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, sessionmaker
from config.dbconfig import Base

class Usinas(Base):
    __tablename__ = 'usinas'

    id = Column('ID', Integer, primary_key = True, autoincrement = True)
    usina = Column('usina', String)
    cliente_id = Column('cliente',  Integer, ForeignKey('clientes.ID'))

    def __repr__(self):
        return f"Usina[id={self.id}, usina={self.usina}]"