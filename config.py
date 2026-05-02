import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey123'
    BLOB_ACCOUNT = os.environ.get('BLOB_ACCOUNT')
    BLOB_STORAGE_KEY = os.environ.get('BLOB_STORAGE_KEY')
    BLOB_CONTAINER = os.environ.get('BLOB_CONTAINER')
    BLOB_CONNECTION_STRING = os.environ.get('BLOB_CONNECTION_STRING')
    SQL_SERVER = os.environ.get('SQL_SERVER')
    SQL_DATABASE = os.environ.get('SQL_DATABASE')
    SQL_USER_NAME = os.environ.get('SQL_USER_NAME')
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD')
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://{0}:{1}@{2}/{3}'.format(
        os.environ.get('SQL_USER_NAME') or '',
        os.environ.get('SQL_PASSWORD') or '',
        os.environ.get('SQL_SERVER') or '',
        os.environ.get('SQL_DATABASE') or ''
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'