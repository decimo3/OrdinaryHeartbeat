''' Module to handle to database access for insert and retrieve data '''
import os
from pyodbc import Connection, connect
from jwt import Heartbeat

class Database:
    ''' Class to manage database access lifecycle '''
    connection: Connection

    def __init__(self) -> None:
        ''' Function to setup and connect to database '''
        db_host = os.environ.get('POSTGRES_HOST')
        db_port = os.environ.get('POSTGRES_PORT')
        db_user = os.environ.get('POSTGRES_USER')
        db_pass = os.environ.get('POSTGRES_PASSWORD')
        if not db_host or not db_port or not db_user or not db_pass:
            raise OSError('Environment variables for database connection is not set!')
        self.connection = connect(
            'Driver={PostgreSQL Unicode(x64)};'
            f'Server={db_host};'
            f'Port={db_port};'
            f'Database=heartbeat;'
            f'Uid={db_user};'
            f'Pwd={db_pass};'
        )
        self.connection.autocommit = True

    def retrieve_heartbeat(self, ip: str = '') -> list[Heartbeat]:
        ''' Function to retrieve all heartbeat data from database '''
        heartbeats: list[Heartbeat] = []
        with self.connection.cursor() as cursor:
            sql = 'SELECT identifier, created_at, created_by, creator_ip, creator_ver FROM heartbeat'
            sql += ' WHERE creator_ip = ?' if ip else ''
            sql += ' ORDER BY identifier DESC LIMIT 1000'
            cursor.execute(sql, (ip,) if ip else ())
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                heartbeats.append(Heartbeat(
                    identifier=row[0],
                    created_at=row[1],
                    created_by=row[2],
                    creator_ip=row[3],
                    creator_ver=row[4]
                ))
        return heartbeats

    def register_heartbeat(self, data: Heartbeat) -> None:
        ''' Function to register one heartbeat data to database '''
        with self.connection.cursor() as cursor:
            sql = 'INSERT INTO heartbeat (created_at, created_by, creator_ip, creator_ver) VALUES (?, ?, ?, ?)'
            cursor.execute(sql, (data.created_at, data.created_by, data.creator_ip, data.creator_ver))

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        self.connection.close()