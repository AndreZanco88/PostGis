from config.dbconfig import DataBase
from config.dbformat import Dbformat
from entities.estacoes import Estacoes
from entities.fluviometricas_geometria import FluviometricasGeometria
from entities.usinas import Usinas
from entities.clientes import Clientes
from entities.corretivas import Corretivas
from entities.classificacao_corretivas import ClassificacaoCorretivas
from sqlalchemy import func    
    
class CorretivasRepository:
    def select_corretivas_layer(self):
        with DataBase() as db:
            try:
                data = db.session.query(Estacoes)\
                    .join(FluviometricasGeometria, Estacoes.id == FluviometricasGeometria.estacao)\
                    .join(Usinas, Estacoes.usina_id == Usinas.id)\
                    .join(Clientes, Usinas.cliente_id == Clientes.id)\
                    .join(Corretivas, Estacoes.id == Corretivas.estacao_id)\
                    .with_entities(
                        Estacoes.estacao,
                        func.ST_AsGeoJSON(FluviometricasGeometria.geometria).label('geometria'),
                        Usinas.usina,
                        Clientes.cliente,
                        Corretivas.id,
                        func.to_char(Corretivas.data_identificacao, 'YYYY-MM-DD"T"HH24:MI:SSZ').label('data_identificacao'),
                        func.to_char(Corretivas.data_resolucao, 'YYYY-MM-DD"T"HH24:MI:SSZ').label('data_resolucao'),
                        func.to_char(Corretivas.data_visita, 'YYYY-MM-DD"T"HH24:MI:SSZ').label('data_visita')
                    )\
                    .all()
                
                colunas = ['Estacao', 'Geometria', 'Usina',  'Cliente', 'Cód. corretiva', 'Data de identificação', 'Data Planejada de visita', 'Data de resolução']

                result = Dbformat().db_format(columns=colunas, db = data)

                return result
            except Exception as exception:
                db.session.rollback()
                raise exception

    def insert_corretiva(self, estacao, **kwargs):
        with DataBase() as db:
            try:
                data_insert = Corretivas(estacao_id=estacao)
                db.session.add(data_insert)
                db.session.commit()
                
                corretiva_id = data_insert.id
                
                if kwargs:
                    try:
                        db.session.query(Corretivas).filter(Corretivas.id == corretiva_id).update(kwargs)
                        db.session.commit()
                    except Exception as exception:
                        db.session.rollback()
                        raise exception
            except Exception as exception:
                db.session.rollback()
                raise exception
            
    def update_corretiva(self, corretiva_id, **kwargs):
        with DataBase() as db:
            for key, value in kwargs.items():
                try:
                    db.session.query(Corretivas).filter(Corretivas.id == corretiva_id).update({key:value})
                    db.session.commit()
                except Exception as exception:
                    db.session.rollback()
                    raise exception
        
    def remove_corretiva(self, corretiva_id):
        with DataBase() as db:
            try:
                db.session.query(Corretivas).filter(Corretivas.id == corretiva_id).delete()
                db.session.commit()
            except Exception as exception:
                db.session.rollback()
                raise exception

