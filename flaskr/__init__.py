import os

from flask import Flask, render_template

from model.host_database import DB_Model


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
	#set up vars from config here
	SECRET_KEY = "Test" #Change to random seed for production, used by flask for signing cookies etc	
    )

    # Link the host database to the web app
    host_database = DB_Model()
    host_database.test_update_hosts(20)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/UI')
    def render_app():
        host_list = host_database.get_hosts()
        print(host_list)
        return render_template('view_screen.html', hosts=host_list)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=80)
