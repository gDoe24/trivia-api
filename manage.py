from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from backend.flaskr import create_app
from backend.models import db

migrate = Migrate(create_app(), db)
manager = Manager(create_app())

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()