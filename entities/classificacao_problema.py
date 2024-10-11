from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, text, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from config.dbconfig import Base

class ClassificacaoProblema(Base):
    __tablename__ = 'tipo_problema'

    id = Column('ID', Integer, primary_key = True, autoincrement = True)
    classificacao = Column('classificacao', String)