from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, text, DateTime
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, sessionmaker
from config.dbconfig import Base

class Estacoes(Base):
    __tablename__ = 'estacoes_hidro'

    id = Column('ID', Integer, primary_key = True, autoincrement = True)
    estacao = Column('estacao', String)
    usina_id = Column('usina', Integer, ForeignKey('usinas.ID'))

    def __repr__(self):
        return f"Estacao [nome={self.estacao}, id={self.id}, usina = {self.usina_id}]"