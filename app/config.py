import os


base_dir = os.path.abspath(os.path.dirname(__name__))


# 通用配置
class Config:
    # 秘钥，禁止使用中文
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'
    # 数据库操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 使用本地库中的bootstrap依赖包
    BOOTSTRAP_SERVE_LOCAL = True
    #文件上传
    MAX_CONTENT_LENGTH=16 * 1024 *1024
    #文件上传的目录
    UPLOADED_PHOTOS_DEST =os.path.join(base_dir,'static/upload')


    # 初始化的方法
    @staticmethod
    def init_app(app):
        pass


# 开发环境配置
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1qaz@WSX@52.199.241.236:3306/flask_movie'
    # 这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名test


# 测试环境配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-test.sqlite')


# 生产环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog.sqlite')


# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    # 默认配置
    'default': DevelopmentConfig
}
