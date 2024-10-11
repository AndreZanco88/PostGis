from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, text, DateTime
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, sessionmaker
from config.dbconfig import Base

class ClassificacaoCorretivas(Base):
    __tablename__ = 'classificacao_corretivas'

    id = Column('ID',Integer, primary_key = True, autoincrement = True)
    classificacao = Column('prioridade', String)

    def __repr__(self):
        return f"Classificação [prioridade={self.classificacao}]"