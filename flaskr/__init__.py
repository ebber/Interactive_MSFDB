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
    view_toggle = 'ports'

    filter_rules = ["ports = (1-1024. 'OPEN')", "ports = (80, 'OPEN')"]

    hardcoded_filters = {
            "IP = 196.*.*.*" : lambda host : False  if "196" in host.ip else True,
            "ports = (80, 'OPEN')" : lambda host : False if len(host.ports) >0 and host.ports[0][0] == "80" else True,
            "ports = (1-1024. 'OPEN')" : lambda host : False if len(host.ports) ==0 else True,
            }

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



    @app.route('/UI')
    def render_app():
        host_list = host_database.get_hosts()

        if view_toggle == "ports":
            host_list.sort(key=lambda host: host.num_ports, reverse=True)
        else:
            host_list.sort(key=lambda host: host.num_ports, reverse=False)

        #apply filter rules
        filtered_host_list = host_list
        for rule in filter_rules:
            try:
                filtered_host_list = filter( hardcoded_filters[rule], filtered_host_list)
            except:
                pass

        print(len(host_list))
        print(len(filtered_host_list))

        return render_template('view_screen.html', hosts=filtered_host_list, filter_list = filter_rules)


    @app.route('/view/ports', methods=['PORTS'])
    def ports_view_rule():
        view_toggle = 'ports'
        return 'success switching to ports view'

    @app.route('/view/purpose', methods=['PURPOSE'])
    def purpose_view_rule():
        view_toggle = 'purpose'
        return 'success switching to purpose view'

    @app.route('/filter/add', methods=['POST'])
    def add_filter_rule():
        filter_text = request.values['rule']
        filter_rules.append(filter_text)
        return 'success adding rule: ' + filter_text

    @app.route('/filter/remove/<filter_idx>', methods=['DELETE'])
    def remove_filter_rule(filter_idx):
        del filter_rules[int(filter_idx)]
        print("rule removed")
        return "successfully removed filter: " + str(filter_idx)

    @app.route('/comment', methods=['POST'])
    def add_comment():
        request_data = request.get_json()
        #return request_data['host_id'] + " : " + request_data['comment']
        return "success"

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=80)
