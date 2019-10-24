# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()
import os
from app import create_app

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
"""
pagination = Posts.query.filter_by(uid=sid).order_by(Posts.timestamp.desc()).paginate(page, per_page=1, error_out=False)
"""

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
application = app.wsgifunc()
# 添加命令行启动控制
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()