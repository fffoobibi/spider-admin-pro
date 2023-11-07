# -*- coding: utf-8 -*-
# ==============================================
# 系统信息接口
# ==============================================
import subprocess

from flask import request

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
def execute_shell():
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
        cursor.close()
        db.close()
