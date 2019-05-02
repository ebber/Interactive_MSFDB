
from model.host_model import host

test_host_model = vars(host())

# prepare_filter :: String -> Maybe([host -> Bool])
def prepare_filter(query_str):
    pass


#port_num
def gen_port_lambda(property_name, property_range):
    print("generating port lambda")

    if property_range.isdigit():
        good_port_lambda = lambda port: port[0] == int(property_range)
    else:
        good_port_lambda = lambda port: property_range in  port[1] 

    return lambda host: True if len(list(filter(good_port_lambda,host["ports"])))>0 else False

def gen_ip_lambda(property_name, property_range):
    print("ip lambda")

    def ipToBin(ip_str):
        octets = map(int, ip_str.split('/')[0].split('.')) # '1.2.3.4'=>[1, 2, 3, 4]
        binary = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(*octets)
        return binary

        

    #TODO: Detect and filter on CIDR Notation or regex 
    CIDR_split = property_range.split("/")
    target_ip = CIDR_split[0]
    if len(CIDR_split) is 1:
        octs = target_ip.split(".")
        rang =32 
        for i in range(0,len(octs)):
            if octs[i] is "*":
                rang-=8
                octs[i] = "1"
        new_target_ip = ".".join(octs)
        return lambda host: True if (ipToBin(new_target_ip)[:rang]) == (ipToBin(host[property_name]) [:rang]) else False

    elif len(CIDR_split) is 2:
        rang = int(CIDR_split[1])
        return lambda host: True if (ipToBin(target_ip)[:rang]) == (ipToBin(host[property_name]) [:rang]) else False
        
    else:
        print(CIDR_split)
        return None
    return None # should never get to this point 

def gen_num_lambda(property_name, property_range):
    print("generating number lambda")
    #notice if format is = vs (x-y) TODO
    return lambda host: True if int(host[property_name]) == int(property_range) else False


def gen_str_lambda(property_name, property_range):
    #TODO (low priority): implement regex
    return lambda host: True if (str(host[property_name])) in (str(property_range)) else False

#parse_component :: String -> Maybe([host -> Bool])
def parse_component(component_string):
    #split on equal
    split_str = component_string.split("=")
    if len(split_str) != 2:
        return "Filter is improperly formatted."
    split_str = list(map(str.strip, split_str))
    property_name = split_str[0]
    property_range = split_str[1]
    #left is property
    if property_name not in test_host_model.keys():
        return "Filter property does not exist"
    if ' ' in property_range:
        return "Filter range is incorrectly inputted"
    #right is range
    switcher = {
            "ports": gen_port_lambda,
            "ip":  gen_ip_lambda,
            "num_ports": gen_num_lambda,
            "OS" : gen_str_lambda #TODO: for some reason this works in the test but doesn't work live. (If it turns into a timesync, Erik has some ideas on why/how to fix)
            }
    r_lamb = switcher.get(property_name, gen_str_lambda) (property_name, property_range) #protected/known to exist because we previously check
    return r_lamb

def parse_querry(querry_str):
    #TODO: Deal with breaking into components
    return parse_component(querry_str)


if __name__ == '__main__':
    #print(parse_component("num_ports=1") (test_host_model))
    print (test_host_model)
    #print(parse_querry("OS=Windows") (test_host_model))
    #print(parse_querry("ports=80") (test_host_model))
    #print(parse_querry("ports=ssh") (test_host_model))
    print(parse_component("ip=192.0.0.1/0") (test_host_model))
    print(parse_component("ip=*.*.*.*") (test_host_model))
    #print(parse_component("num_ports=3") (test_host_model))
