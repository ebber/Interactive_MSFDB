import mock_host_data as mock
import random

class host:

    def __init__(self,ip = False, OS = False, ports = False ,services = False, purpose = False, comments=""):
        if ip:
            self.initialize(ip, OS, ports, purpose)
        else:
            self.init_test()
            

    #ports -> [port] -> [(port num, service,info, state)]
    def initialize(self, ip, OS, ports, purpose):
        self.ip = ip
        self.OS = OS
        self.ports = ports 
        self.purpose = purpose

    def init_test(self):

        fake_ip = str(random.randint(0,256)) + "." + str(random.randint(0,256)) +"." + str(random.randint(0,256)) +"."+ str(random.randint(0,256))
        fake_OS = mock.OS[random.randint(0,len(mock.OS)-1)]
        fake_ports = []
        for i in range(0,5):
            if 6< random.randint(0,10):
                fake_ports.append(mock.Ports[random.randint(0,len(mock.Ports)-1)])

        fake_purpose = mock.Purposes[random.randint(0, len(mock.Purposes)-1)]
        self.initialize(fake_ip, fake_OS,fake_ports, fake_purpose)

    def toString(self):
        return "IP:" + self.ip + " OS:" + self.OS + "Ports open:" +str(len(self.ports)) + " Purpose:" + self.purpose


if __name__ == '__main__':
    t_host = host() 
    print(t_host.toString())
