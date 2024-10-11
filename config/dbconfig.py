from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 

Base = declarative_base()

class DataBase:
    def __init__(self) -> None:
        self.__connection_info = {
            'dbname': 'Construserv',
            'user': 'postgres',
            'password': '8543',
            'host': 'localhost',
            'port': 5432
        }

        self.__connection_string = f'''postgresql+psycopg2://{self.__connection_info['user']}:{self.__connection_info['password']}
                                    @{self.__connection_info['host']}:{self.__connection_info['port']}/{self.__connection_info['dbname']}'''
        
        self.engine = self.__create_engine()

        self.session = None


    def __create_engine(self):
        engine = create_engine(self.__connection_string)
        return engine
    
    def __enter__(self):
        session = sessionmaker(bind=self.engine)
        self.session = session()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.session.close()