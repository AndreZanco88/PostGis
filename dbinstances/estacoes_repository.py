from config.dbconfig import DataBase
from config.dbformat import Dbformat
from entities.estacoes import Estacoes
from entities.fluviometricas_geometria import FluviometricasGeometria
from entities.usinas import Usinas
from entities.clientes import Clientes
from entities.corretivas import Corretivas
from sqlalchemy import func

class EstacoesRepository:
    def select(self):
        with DataBase() as db:
            try:
                data = db.session.query(Estacoes)\
                    .join(Usinas, Estacoes.usina_id == Usinas.id)\
                    .join(Clientes, Usinas.cliente_id == Clientes.id)\
                    .with_entities(
                        Estacoes.estacao,
                        Usinas.usina,
                        Clientes.cliente
                    ).all()
                return data
            except Exception as exception:
                db.session.rollback()
                raise exception
    
    def select_geometry(self):
        with DataBase() as db:
            try:
                data = db.session.query(Estacoes)\
                    .join(FluviometricasGeometria, Estacoes.id == FluviometricasGeometria.estacao)\
                    .with_entities(
                        Estacoes.estacao,
                        func.ST_AsGeoJSON(FluviometricasGeometria.geometria).label('geometria')
                    )\
                    .all()
                return data
            except Exception as exception:
                db.session.rollback()
                raise exception
     
    def select_estacoeslayer(self):
        with DataBase() as db:
            try:
                data = db.session.query(Estacoes)\
                    .join(FluviometricasGeometria, Estacoes.id == FluviometricasGeometria.estacao)\
                    .join(Usinas, Estacoes.usina_id == Usinas.id)\
                    .join(Clientes, Usinas.cliente_id == Clientes.id)\
                    .with_entities(
                        Estacoes.estacao,
                        func.ST_AsGeoJSON(FluviometricasGeometria.geometria).label('geometria'),
                        Usinas.usina,
                        Clientes.cliente
                    )\
                    .all()
                
                colunas = ['Estacoes', 'Geometria', 'Usina',  'Cliente']

                result = Dbformat().db_format(columns=colunas, db = data)

                return result
            except Exception as exception:
                db.session.rollback()
                raise exception
            
    
        
    