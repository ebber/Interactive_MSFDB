import model.mock_host_data as mock
import random

class host:

    def __init__(self,ident = -1, ip = False, OS = False, ports = False ,services = False, purpose = False, comments=""):

        if ip:
            self.initialize(ip, ident, OS, ports, purpose, comments)
        else:
            self.init_test()
            

    #ports -> [port] -> [(port num, service,info, state)]
    def initialize(self,ident, ip, OS, ports, purpose, comments):
        self.ip = str(ip)
        self.OS = OS
        self.ports = ports 
        self.num_ports = str(len(ports))
        self.purpose = purpose
        self.comments = comments

        if ident == -1:
            self.id = random.randint(0,200)
        else:
            self.id = ident
        self.id = str(self.id)

    def init_test(self):

        fake_ip = str(random.randint(0,256)) + "." + str(random.randint(0,256)) +"." + str(random.randint(0,256)) +"."+ str(random.randint(0,256))
        fake_OS = mock.OS[random.randint(0,len(mock.OS)-1)]
        fake_ports = []
        for i in range(0,5):
            if 6< random.randint(0,10):
                fake_ports.append(mock.Ports[random.randint(0,len(mock.Ports)-1)])

        fake_purpose = mock.Purposes[random.randint(0, len(mock.Purposes)-1)]
        self.initialize(ident=-1,ip=fake_ip, OS=fake_OS, ports=fake_ports, purpose=fake_purpose, comments = "This is a test host")

    def toString(self):
        return "IP:" + self.ip + " OS:" + self.OS + "Ports open:" +str(len(self.ports)) + " Purpose:" + self.purpose


if __name__ == '__main__':
    t_host = host() 
    print(t_host.toString())
