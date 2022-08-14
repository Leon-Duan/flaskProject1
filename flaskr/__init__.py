import os
from flask import Flask


def create_app(test_config=None):
    # 创建FLASK实例，命名为app。
    app = Flask(__name__, instance_relative_config=True)
    # __name__内置变量
    # 来，配置一下app
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    # 此处是测试时加载配置的方法
    if test_config is None:
        # 从文件加载配置，我们没有
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 确保实例文件存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass  # 不存在直接跳过去

    # 加载一个页面
    @app.route('/')
    def index():
        return '''
        <title>Leon's Web underway</title>
        <head1>Learning, Nothing I can tell you now</head1>
        '''

    from.import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
