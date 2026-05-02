import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey123'

    BLOB_ACCOUNT = os.environ.get('BLOB_ACCOUNT') or 'cmsstorage123'
    BLOB_STORAGE_KEY = os.environ.get('BLOB_STORAGE_KEY') or '3TkbEmHuydVuB95BIK5qEdwY80vMJht+5z1J1mpcsC/KGkSXhvtVHW/W79OZRLgrVphGSwdSuILA+AStbBNkOQ=='
    BLOB_CONTAINER = os.environ.get('BLOB_CONTAINER') or 'images'
    BLOB_CONNECTION_STRING = os.environ.get('BLOB_CONNECTION_STRING') or 'DefaultEndpointsProtocol=https;AccountName=cmsstorage123;AccountKey=3TkbEmHuydVuB95BIK5qEdwY80vMJht+5z1J1mpcsC/KGkSXhvtVHW/W79OZRLgrVphGSwdSuILA+AStbBNkOQ==;EndpointSuffix=core.windows.net'

    SQL_SERVER = os.environ.get('SQL_SERVER') or 'cms-server-122.database.windows.net'
    SQL_DATABASE = os.environ.get('SQL_DATABASE') or 'cms'
    SQL_USER_NAME = os.environ.get('SQL_USER_NAME') or 'cmsadmin'
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD') or 'CMS4dmin!'

    CLIENT_ID = os.environ.get('CLIENT_ID') or '4ce57ae1-64f6-4524-8854-ee9c53773089'
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET') or 'yAE8Q~GgKJeaYyqXm_eSU-X2ruTa4TV5V4.hndaq'

    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://{0}:{1}@{2}/{3}'.format(
        os.environ.get('SQL_USER_NAME') or 'cmsadmin',
        os.environ.get('SQL_PASSWORD') or 'CMS4dmin!',
        os.environ.get('SQL_SERVER') or 'cms-server-122.database.windows.net',
        os.environ.get('SQL_DATABASE') or 'cms'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'