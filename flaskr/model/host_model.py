class host:

    def __init__(self,ip = False, OS = False, ports = False ,services = False, purpose = False):
        if ip:
            self.initialize(ip, OS, ports, services, purpose)
        else:
            self.init_test()
            

    def initialize(self, ip, OS, ports, services, purpose):
        self.ip = ip
        self.OS = OS
        self.ports = ports 
        self.services = services
        self.purpose = purpose

    def init_test(self):
        self.initialize("127.0.0.1", "OSX", [22], "sshd v2.3.1", "auth server")

if __name__ == '__main__':
    t_host = host() 
    print(t_host)
