class host:

    def __init__(self,ip = False, OS = False, ports = False ,services = False, purpose = False, comments=""):
        if ip:
            self.initialize(ip, OS, ports, purpose)
        else:
            self.init_test()
            

    #ports -> [port] -> [(port num, service, state)]
    def initialize(self, ip, OS, ports, purpose):
        self.ip = ip
        self.OS = OS
        self.ports = ports 
        self.purpose = purpose

    def init_test(self):
        self.initialize("127.0.0.1", "Linux", [(22, "sshd v2.3.1", "OPEN")], "auth server")

    def toString(self):
        return "IP:" + self.ip + " OS:" + self.OS

if __name__ == '__main__':
    t_host = host() 
    print(t_host.toString())
