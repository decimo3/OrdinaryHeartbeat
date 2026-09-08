''' Script to register heartbeat log from applications, worksheets and dashboards '''
from flask import Flask, request
from dba import Database
from jwt import Heartbeat

app = Flask(__name__)

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
        database.register_heartbeat(heartbeat)
    return 'OK', 201