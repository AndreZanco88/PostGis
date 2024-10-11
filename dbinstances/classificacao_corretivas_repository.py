from config.dbconfig import DataBase
from entities.classificacao_corretivas import ClassificacaoCorretivas

class ClassificacaoCorretivasRepository:
    def select(self):
        with DataBase() as db:
            try:
                data = db.session.query(ClassificacaoCorretivas).all()
                return data
            except Exception as exception:
                db.session.rollback()
                raise exception