from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Text, DateTime
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, sessionmaker
from config.dbconfig import Base

class Corretivas(Base):
    __tablename__ = 'corretivas'

    id = Column('id', Integer, primary_key = True, autoincrement = True)
    estacao_id = Column('estacao', Integer, ForeignKey('estacoes_hidro.ID'), primary_key=True)
    prioridade_id = Column('prioridade', Integer, ForeignKey('classificacao_corretivas.ID'))
    data_identificacao = Column('data_identificacao', DateTime)
    data_visita = Column('data_planejada', DateTime)
    data_resolucao = Column('data_resolucao', DateTime)
    descricao = Column('descricao', Text)
    classificacao_problema = Column('classificacao_problema', Integer, ForeignKey('tipo_problema.ID'))

