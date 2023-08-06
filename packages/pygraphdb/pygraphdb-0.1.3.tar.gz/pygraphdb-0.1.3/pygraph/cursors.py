# -*- coding: UTF-8 -*-
# @Time : 2021/11/15 下午6:04 
# @Author : 刘洪波
import requests


class Cursor(object):
    def __init__(self, db_url, authorization):
        self.db_url = db_url
        self.authorization = authorization

    def execute(self, sparql):
        """
        执行 sparql
        :param sparql: 例 "SELECT ?s ?p ?o WHERE {?s ?p ?o .} LIMIT 100"
        :return:
        """
        if self.db_url is None or self.authorization is None:
            raise BaseException('Cursor is closed')
        params = self.check_key(sparql)
        return requests.get(self.db_url, headers={'Authorization': self.authorization}, params=params).text

    @staticmethod
    def check_key(sparql):
        """
        校验sparql里的关键字
        :param sparql:
        :return:
        """
        upper_sparql = sparql.upper()
        query = ['SELECT', 'CONSTRUCT', 'ASK', 'DESCRIBE']
        update = ['INSERT', 'DELETE']
        for q in query:
            if q in upper_sparql:
                params = {'query': sparql}
                return params
        for u in update:
            if u in upper_sparql:
                params = {'update': sparql}
                return params
        raise ValueError('sparql error, Keyword deletion')

    def close(self):
        self.db_url = None
        self.authorization = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

