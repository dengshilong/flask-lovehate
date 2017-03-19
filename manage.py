#!/usr/bin/env python
# pylint: disable=wrong-import-position
import os


if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]
from app import create_app, db
from app.models import User, Post, Category
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


APP = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(APP)
migrate = Migrate(APP, db)


def make_shell_context():
    return dict(app=APP, db=db, User=User, Post=Post, Category=Category)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def createsuperuser(email, username, password):
    """create superuser"""
    user = User(email=email, username=username, password=password,
                is_administrator=True, confirmed=True)
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
