import os

from flask import Flask, render_template, request

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
        return render_template('view_screen.html', hosts=host_list)

    @app.route('/filter/add', methods=['POST'])
    def add_filter_rule():
        filter_text = request.values['rule']
        return 'success addeding rule: ' + filter_text

    @app.route('/filter/remove/<filter_id>')
    def remove_filter_rule(filter_id):
        return "successfully removed filter: " + str(filter_id)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=80)
