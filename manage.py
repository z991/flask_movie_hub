import os
from app import create_app

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
application = app.wsgifunc()
# 添加命令行启动控制
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    app.run()