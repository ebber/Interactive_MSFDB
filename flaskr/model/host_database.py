import os
import subprocess
import model.db_config
from psycopg2 import connect
from model.host_model import host

class DB_Model:
    def __init__(self):
        #connect to real db here
        try:
            conn_string = "dbname='"+db_config.DB_NAME+"' user='"+db_config.DB_USER+"' password='"+db_config.DB_PASSWORD+"'"
            conn = connect(conn_string)
            self.cursor = conn.cursor()
            self.cursor.execute("SELECT table_name FROM information_schema.tables")
        except :
            print("DB connect failed")
            self.connected = False


        self.hosts = []
        self.view_toggle = 'ports'

    def get_hosts(self):
        return self.hosts

    def get_view(self):
        return self.view_toggle

    def set_view(self, value):
        self.view_toggle = value

    def does_host_exist(self, ident):
        hosts = self.get_hosts()
        for host in hosts:
            if host.ident == ident:
                return True
        return False

    #update from the DB
    def update_hosts(self):
        if not self.connected:
            print("DB not connected, use test_update_hosts")
            return False
        q_string = "SELECT id, address, os_family, service_count, purpose, comments FROM public.hosts"
        self.cursor.execute(q_string)
        rows = self.cursor.fetchall()

        
        for row in rows:
            host_ports = self.get_host_port_info(row[0]) #id
            if not self.does_host_exist(row[0]):
                self.hosts.append(host(ident=row[0],ip=row[1], OS=row[2], ports=host_ports, purpose=row[4], comments=row[5]))
        return True

    def test_update_hosts(self, num=1):
        port_l = [ 
         (20, "telnet", "telnet info", "OPEN"),
         (22, "SSH", "SSH info", "OPEN"),
         (53, "DNS", "DNS info", "OPEN"),
         (80, "HTTP", "HTTP info", "OPEN"),
         (3306, "SQL", "mySQL v2.1.0", "OPEN")]
        test_host = host(ident=1, ip="194.168.0.1", OS="Linux", ports=port_l, purpose = "DB", comments="This is a test host")
        for i in range(0,num):
            self.hosts.append(host())
        self.hosts.append(test_host)

    def get_host_port_info(self, host_id):
        q_string = "SELECT port, name, info, state FROM public.services WHERE services.host_id = " + str(host_id)
        self.cursor.execute(q_string)
        port_list = self.cursor.fetchall()
        if port_list is None:
            port_list = []
        return port_list


    #Scanning stuff
    def scan_host(self, host_ip):
        scan_str = "nmap -A "+host_ip
        print("scanning: " +host_ip)
        self.run_scan(scan_str)
        return True



    def scan(self):
        hosts = self.get_hosts()
        for host in hosts:
            self.scan_host(host.ip)
        return True

    def discover_network(self):
        print("discovering network")
        res=subprocess.check_output(["arp-scan", "-l"]).split("\n")[2:-4]
        ips = map (lambda x: x.split('\t')[0].strip(), res)
        scan_str = "nmap " + " ".join(ips)
        return self.run_scan(scan_str)




    def run_scan(self, scan_text):
        print(scan_text.split("nmap "))
        opts = scan_text.split("nmap ")[-1]
        new_scan = "nmap -oX nmap_scan.tmp " + opts
        os.system(new_scan)
        os.system('msfconsole -q -x "db_import nmap_scan.tmp; quit;"')
        self.update_hosts()
        return True



if __name__ == '__main__':
    test_DB = DB_Model()
    test_DB.test_update_hosts(10)
    for host in test_DB.get_hosts():
        print(host.toString())
