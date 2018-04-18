'''manage.py - Database migration commands'''
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from application import db, create_app

#initialize the app with all its configurations
app = create_app(config_name='development')
migrate = Migrate(app, db)
#create an instance of class to handle all commands
manager = Manager(app)

manager.add_command('db', MigrateCommand)

#define command for testing called "test"
@manager.command
def test():
    '''runs unittest without test coverage'''
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
