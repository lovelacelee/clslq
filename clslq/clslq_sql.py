# -*- encoding:utf-8 -*-
'''
MIT License

Copyright (c) 2021 Connard Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from sqlalchemy import create_engine
# text SQL statement
from sqlalchemy import text
from sqlalchemy.engine import url
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import BigInteger
from contextlib import contextmanager
from sqlalchemy.orm import relationship

# Base Data object
ClslqBaseTable = declarative_base()

class ClslqSql(object):
    """
    ClslqSql is a wrapper class for SQLAlchemy
    """
    __engine = None
    __session = None
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()

    def create(self, dburl):
        """
        dialect+driver://username:password@host:port/database
        password is URL encoded(import urllib.parse)
        ------------------------------------------------------
        sqlite://<nohostname>/<path>, where <path> is relative
        sqlite:///foo.db, means foo.db in current path
        sqlte+pysqlte:///:memory:
        sqlite:////absolute/path/to/foo.db, absolute after '///'
        sqlite:///C:\\path\\to\\foo.db, Windows absolute path
        r'sqlite:///C:\\path\\to\\foo.db', Windows alternative using raw string
        engine = create_engine('sqlite://') Using SQLite :memory:

        postgresql://scott:tiger@localhost:5432/mydatabase
        postgresql+psycopg2://scott:tiger@localhost/mydatabase
        postgresql+pg8000://scott:tiger@localhost/mydatabase

        mysql://scott:tiger@localhost/foo
        mysql+mysqldb://scott:tiger@localhost/foo
        mysql+pymysql://scott:tiger@localhost/foo

        oracle://scott:tiger@127.0.0.1:1521/sidname
        oracle+cx_oracle://scott:tiger@tnsname

        mssql+pyodbc://scott:tiger@mydsn
        mssql+pymssql://scott:tiger@hostname:port/dbname
        """
        self.__engine = create_engine(dburl, echo=True)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def init(self, driver, user, passwd, host, port, dbname):
        self.create(url.URL(
            drivername=driver, 
            username=user,
            password=passwd,
            host=host,
            port=port,
            database=dbname
        ))

    def create_table(self, table=ClslqBaseTable):
        """
        Create Table use MetaData, Column, and https://www.osgeo.cn/sqlalchemy/core/type_basics.html
        """
        try:
            table.metadata.create_all(self.__engine)
        except Exception as e:
            raise

    def insert(self, item=None):
        if not item:
            raise Exception('item is required')
        dbsession = sessionmaker(bind=self.__engine)
        session = dbsession()
        try:
            session.add(item)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete(self, item=None):
        if not item:
            raise Exception('item is required')
        dbsession = sessionmaker(bind=self.__engine)
        session = dbsession()
        try:
            session.delete(item)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    def query(self, table=None):
        '''
        How to filter
        result.filter(Table.attr == value)
        How to update
        result.filter(Table.attr == value).update({'attr': 'new_value'})
        filter().delete()
        filter().all()
        '''
        if not table:
            raise Exception('table is required')
        session = self.__session()
        try:
            result = session.query(table)
        except Exception as e:
            raise e
        finally:
            session.close()
        return result
    
    def commit(self):
        session = self.__session()
        session.commit()