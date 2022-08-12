import os
from flask import Flask

def create_app(test_config=None):
    #创建FLASK实例，命名为app。
    app = Flask(__name__, instance_relative_config=True)
        ''' __name__声明位置所在，后面那个是说配置文件我这里也写了'''
    #来，配置一下app
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    )
         #mapping，使用flask包自带的配置，这里设置密匙为dev，设置了数据库的路径

    #此处是测试时加载配置的方法
    if test_config is None:
        #从文件加载配置，我们没有
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    #确保实例文件存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass   #不存在直接跳过去

    #加载一个页面
    @app.route('/hello')
    def hello():
        return 'Hello World!'

    return app