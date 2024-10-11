import psycopg2

class GisDatabase:
    def __init__(self) -> None:
        self.conn_info = {
            'dbname': 'Construserv',   
            'user': 'postgres',           
            'password': '85433458',         
            'host': 'localhost',        
            'port': 5432  
        }
        try:
            self.conn = psycopg2.connect(**self.conn_info)
            print("Conexão estabelecida com sucesso!")
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")


db = GisDatabase()

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, text, DateTime
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, sessionmaker
import pandas as pd

# Configurar a conexão com o banco de dados
conn_info = {
    'dbname': 'Construserv',
    'user': 'postgres',
    'password': '85433458',
    'host': 'localhost',
    'port': 5432
}
conn_string = f"postgresql+psycopg2://{conn_info['user']}:{conn_info['password']}@{conn_info['host']}:{conn_info['port']}/{conn_info['dbname']}"
engine = create_engine(conn_string)

Base = declarative_base()

class Estacao(Base):
    __tablename__ = 'estacoes'

    id = Column('ID',Integer, primary_key = True, autoincrement = True)
    estacao = Column('estacoes.id', String)

class ClassificacaoCorretivas(Base):
    __tablename__ = 'classificacao_corretivas'

    id = Column(Integer, primary_key = True, autoincrement = True)
    classificacao = Column(String)

class CorretivasTrocas(Base):
    __tablename__ = 'andamento_corretivas'

    id = Column(Integer, primary_key = True, autoincrement = True)
    classificacao = Column(String)


class corretivasTime(Base):
    __tablename__ = 'corretiva_datas'

class Usinas(Base):
    __tablename__ = 'usinas'

    id = Column(Integer, primary_key = True, autoincrement = True)
    usina = Column(String)

class clientes(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key = True, autoincrement = True)
    cliente = Column(String)


class FluviometricasGeometria(Base):
    __tablename__ = 'geometria_estacoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    geometria = Column(Geometry('POINT', srid=4326))

class classificaoCorretivasEstacoes(Base):
    __tablename__ = 'classificacao_corretivas_estacoes'

    estacao_id = Column(Integer, ForeignKey('estacoes.id'), primary_key=True)
    prioridade_id = Column(Integer, ForeignKey('classificacao_corretivas.id'), primary_key=True)
    data_atribuicao = Column(DateTime)

class Corretivas(Base):
    __tablename__ = 'corretivas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    data_identificacao = Column(DateTime)
    data_planejada = Column(DateTime)
    data_resolucao = Column(DateTime)

    estacao_id = relationship('Estacao', backref = 'estacoes')

class Corretiva_tipo_problema(Base):
    __tablename__ = 'tipo_problema'
    
try:
    Base.metadata.create_all(engine)
    print("Tabela 'Corretivas' criada com sucesso.")
except Exception as e:
    print(f"Ocorreu um erro ao criar a tabela: {e}")

table = pd.read_excel('C:\\Users\\andre.zanco\\Documents\\prototipo construserv\\Lista_estações_revisadas.xlsx')

table_2 = pd.DataFrame()

table_2['estacoes'] = table['ESTACAO']

table_2['ID'] = [i for i in range(1, len(table['ESTACAO']) + 1)]

table_2[['ID', 'estacoes']].to_sql('estacoes', engine, if_exists='replace', index=False)

table['ID'] = [i for i in range(1, len(table['ESTACAO']) + 1)]

pr = {
    'ID': [1,2,3], 'prioridade':['BAIXA', 'MÉDIA', 'ALTA']
}
prioridades = pd.DataFrame(data = pr)

prioridades[['ID', 'prioridade']].to_sql('classificacao_corretivas', engine, if_exists='replace', index=False)

andamento = {
    'ID':[1,2,3,4], 'classificacao':['data_identificação', 'data_planejada', 'data_visita', 'data_conclusao']
}

ada = pd.DataFrame(data = andamento)

ada[['ID', 'classificacao']].to_sql('andamento_corretivas', engine, if_exists='replace', index=False)

usinas = table['USINA'].unique()

table_usinas = pd.DataFrame()

table_usinas['ID'] = [i for i in range(1, len(usinas) + 1)]
table_usinas['usina'] =  usinas

table_usinas[['ID', 'usina']].to_sql('usinas', engine, if_exists='replace', index=False)

clientes = table['CLIENTE'].unique()

table_clientes = pd.DataFrame()

table_clientes['ID'] = [i for i in range(1, len(clientes)+1)]
table_clientes['cliente'] = clientes

table_clientes[['ID', 'cliente']].to_sql('clientes', engine, if_exists='replace', index=False)

import geopandas as gpd
from shapely.geometry import Point

table['X'], table['Y'] = table['X'].astype(float), table['Y'].astype(float)
table['geometry'] = table.apply(lambda row: Point(row['X'], row['Y']), axis=1)

ddf = gpd.GeoDataFrame(table, geometry='geometry')

ddf['estacao'] = [i for  i in range(1, len(table['ESTACAO']) + 1)]

for i in ddf.columns:
    if i != 'estacao' and i != 'geometry':
        ddf = ddf.drop(columns=[i])

with engine.connect() as conn:
    ddf.to_postgis(name = 'fluviometricas_geometria', con=engine, if_exists='replace', index = False)

problemas_classificao = pd.read_excel('C:\\Users\\andre.zanco\\Documents\\prototipo construserv\\classificacao_problemas.xlsx')

