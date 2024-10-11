from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, text, DateTime
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, sessionmaker
from config.dbconfig import Base

class FluviometricasGeometria(Base):
    __tablename__ = 'fluviometricas_geometria'

    estacao = Column(Integer, ForeignKey('estacoes.id'), primary_key=True)
    geometria = Column('geometry', Geometry('POINT', srid=4326))
    
    def __repr__(self):
        return f"Estacao [id={self.estacao}, geometria={self.geometria.wkt}]"