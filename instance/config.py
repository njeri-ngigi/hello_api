'''config.py - Database configurations'''

class Config(object):
    '''parent config file'''
    DEBUG = True
    SECRET_KEY = 'HACHoooaadsf8960-38-(*&^W(*kdfll'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:testme@localhost:5432/hello_api'
    
class DevelopmentConfig(Config):
    '''Configurations for development'''
    Debug = True

class TestingConfig(Config):
    '''configurations for testing with a separate test database'''
    TESTING = True
    Debug = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/test_db'

app_config =
    'development' : DevelopmentConfig,
    'testing' : TestingConfig
}
