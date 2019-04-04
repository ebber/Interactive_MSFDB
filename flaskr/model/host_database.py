from host_model import host
import db_config
from psycopg2 import connect

class DB_Model:

    def __init__(self):
        #connect to real db here
        conn_string = "dbname='"+db_config.DB_NAME+"' user='"+db_config.DB_USER+"' password='"+db_config.DB_PASSWORD+"'"
        conn = connect(conn_string)
        self.cursor = conn.cursor()
        self.cursor.execute("SELECT table_name FROM information_schema.tables")


        self.hosts = []

    def get_hosts(self):
        return self.hosts

    #update from the DB
    def update_hosts(self):
        q_string = "SELECT address, os_family, service_count, purpose, comments FROM public.hosts"
        self.cursor.execute(q_string)
        for row in self.cursor:
           self.hosts.append(host(row[0], row[1], row[2], row[3], row[4])) 

    def test_update_hosts(self, num=1):
        for i in range(0,num):
            self.hosts.append(host())



if __name__ == '__main__':
    test_DB = DB_Model()
    test_DB.update_hosts()
    for host in test_DB.get_hosts():
        print host.toString()
