# -*- coding: utf-8 -*-
# ==============================================
# 系统信息接口
# ==============================================
import subprocess

from flask import request, send_file

from spider_admin_pro.utils.flask_ext.flask_app import BlueprintAppApi
from spider_admin_pro.service.auth_service import AuthService
from spider_admin_pro.service.system_data_service import SystemDataService

system_api = BlueprintAppApi("system", __name__)


@system_api.before_request
def before_request():
    token = request.headers.get('Token')
    AuthService.check_token(token)


@system_api.post('/systemInfo')
def get_system_info():
    return SystemDataService.get_system_info()


@system_api.post("/systemData")
def get_system_data():
    return SystemDataService.get_system_data()


@system_api.post("/systemConfig")
def get_system_config():
    return SystemDataService.get_system_config()


@system_api.post("/systemCall")
def execute_shell():
    command = request.json.get("command")
    timeout = request.json.get("timeout")
    pipe = subprocess.Popen(command, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    out, _ = pipe.communicate(timeout=timeout)
    return {'out': out.decode()}


@system_api.post("/systemCallEngineSelect")
def execute_select():
    database = request.json.get("database")
    sql = request.json.get("sql")
    import pymysql
    from prettytable import from_db_cursor
    db = pymysql.connect(**database)
    try:
        db.begin()
        cursor = db.cursor()
        cursor.execute(sql)
        table = from_db_cursor(cursor)
        return {'out': table.get_string()}
    finally:
        db.rollback()
        try:
            cursor.close()
        finally:
            db.close()


@system_api.post('/download_file')
def download_file():
    file_path = request.json.get('file_path')
    return send_file(file_path)


@system_api.post("/systemCallEngineQuery")
def execute_query():
    database = request.json.get("database")
    sql = request.json.get("sql")
    import pymysql
    db = pymysql.connect(**database)
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        return {'out': data}
    finally:
        cursor.close()
        db.close()


@system_api.post("/systemCallEngineQueryDict")
def execute_query_dict():
    database = request.json.get("database")
    sql = request.json.get("sql")
    import pymysql
    db = pymysql.connect(**database, cursorclass=pymysql.cursors.DictCursor)
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        return {'out': data}
    finally:
        cursor.close()
        db.close()


@system_api.post("/systemCallEngineExecute")
def execute_commit():
    database = request.json.get("database")
    sql = request.json.get("sql")
    import pymysql
    db = pymysql.connect(**database)
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return {'out': 'success'}
    except:
        db.rollback()
    finally:
        cursor.close()
        db.close()
