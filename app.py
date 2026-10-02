''' Script to register heartbeat log from applications, worksheets and dashboards '''
import logging
from datetime import datetime, timedelta
from flask import Flask, request
from dba import Database
from jwt import Heartbeat

app = Flask(__name__)

logging.basicConfig(
    filename='heartbeat.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s [em %(pathname)s:%(lineno)d]'
)

@app.get('/')
def retrieve():
    with Database() as database:
        return database.retrieve_heartbeat()

@app.post('/')
def register():
    json_data = request.get_json()
    if (
        not request.remote_addr or
        not json_data.get('created_at') or
        not json_data.get('created_by') or
        not json_data.get('creator_ver')
    ):
        return 'One or more info are not sent!', 400
    heartbeat = Heartbeat(
        identifier=0,
        creator_ip=request.remote_addr,
        created_at=json_data['created_at'],
        created_by=json_data['created_by'],
        creator_ver=json_data['creator_ver'],
    )
    with Database() as database:
        tolerance = datetime.now() + timedelta(minutes=-1)
        heartbeats = database.retrieve_heartbeat(request.remote_addr)
        if not heartbeats or heartbeats[0].created_at < tolerance:
            database.register_heartbeat(heartbeat)
    return 'OK', 201

@app.errorhandler(Exception)
def handle_exception(e):
    # Grava o erro e a stack trace completa no arquivo erro_500.log
    app.logger.error("Exceção não tratada capturada:", exc_info=e)
    return "Erro interno no servidor. Verifique com o administrador", 500
