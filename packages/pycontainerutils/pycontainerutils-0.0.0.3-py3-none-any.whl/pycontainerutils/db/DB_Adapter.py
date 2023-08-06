"""
DB 와 연결하는 부분
"""

import pandas as pd

from sqlalchemy.orm.session import sessionmaker

from logging import getLogger

from pycontainerutils.db.BaseDB_Adapter import BaseDBAdapter

logger = getLogger(__name__)


class DBAdapter(BaseDBAdapter):
    """
    데이터를 사용하는 엔진
    해당 데이터를 다루는 모든 조작을 담당
    """

    def __init__(self, name, db_name=None, direct=None):
        super().__init__()
        # 이름 설정
        self.name = name
        self.register_info(db_name=db_name, direct=direct)

    def execute_sql(self, sql: str):
        """
        sql문 단순 실행
        :param sql:
        :return:
        """
        print(f"{self.name} : {sql}")
        session = self.session_maker()
        try:
            session.execute(sql)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"execute_sql fail \n"
                         f"{self.name} engine {self.db_name} - {self.engine_info}")
            raise e
        finally:
            session.close()

    def fetch_data_by_sql(self, sql: str):
        """
        sql문 단순 실행
        :param sql:
        :return:
        """
        print(f"{self.name} : {sql}")
        session = self.session_maker()
        try:
            result_proxy = session.execute(sql)
            return result_proxy.fetchall()
        except Exception as e:
            session.rollback()
            logger.error(f"execute_sql fail \n"
                         f"{self.name} engine {self.db_name} - {self.engine_info}")
            raise e
        finally:
            session.close()

    def fetch_df_by_sql(self, sql: str):
        """
        sql문 단순 실행
        :param sql:
        :return:
        """
        print(f"{self.name} : {sql}")
        session = self.session_maker()
        try:
            data = pd.read_sql(sql, session.bind)
            return data
        except Exception as e:
            session.rollback()
            logger.error(f"execute_sql fail\n"
                         f"{self.name} engine {self.db_name} - {self.engine_info}")
            raise e
        finally:
            session.close()

    def insert_df(self, table_name: str, data: pd.DataFrame, **kwargs):
        data.to_sql(
            table_name,
            self.engine,
            index=False,
            if_exists='append',
            **kwargs
        )
