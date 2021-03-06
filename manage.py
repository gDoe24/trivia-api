from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from backend.flaskr import APP
from backend.flaskr.models import db

migrate = Migrate(APP, db)
manager = Manager(APP)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()