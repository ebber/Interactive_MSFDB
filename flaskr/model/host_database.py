from host_model import host

class DB_Model:

    def __init__(self):
        #connect to real db here
        self.hosts = []

    def get_hosts(self):
        return self.hosts

    #update from the DB
    def update_hosts(self):
        pass

    def test_update_hosts(self, num=1):
        for i in range(0,num):
            self.hosts.append(host())



if __name__ == '__main__':
    test_DB = DB_Model()
    test_DB.test_update_hosts()
    for host in test_DB.get_hosts():
        print host.toString()
