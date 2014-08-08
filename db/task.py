#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-08-08 19:53:09

import time
import logging
import umsgpack
import mysql.connector

import config
from libs import utils
from basedb import BaseDB

class TaskDB(BaseDB):
    '''
    task db

    id, tplid, userid, disabled, init_env, env, session, last_success, success_count, failed_count, last_failed, next, ctime, mtime
    '''
    __tablename__ = 'task'

    def __init__(self, host=config.mysql.host, port=config.mysql.port,
            database=config.mysql.database, user=config.mysql.user, passwd=config.mysql.passwd):
        self.conn = mysql.connector.connect(user=user, password=passwd, host=host, port=port, database=database)

    @property
    def dbcur(self):
        return self.conn.cursor()

    def add(self, tplid, userid, env):
        now = time.time()

        insert = dict(
                tplid = tplid,
                userid = userid,
                disabled = 0,
                init_env = env,
                last_success = None,
                last_failed = None,
                success_count = 0,
                failed_count = 0,
                next = None,
                ctime = now,
                mtime = now,
                )
        self._insert(**insert)

    def mod(self, id, **kwargs):
        assert 'id' not in kwargs, 'id not modifiable'
        assert 'ctime' not in kwargs, 'ctime not modifiable'

        kwargs['mtime'] = time.time()
        return self._update(where="id=%s", where_values=(id, ), **kwargs)

    def get(self, id, fields=None):
        for tpl in self._select2dic(what=fields, where='id=%s', where_values=(id, )):
            return tpl