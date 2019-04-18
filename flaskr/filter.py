


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
    #TODO: Detect and filter on CIDR Notation or regex 
    return (lambda x: True)

def gen_num_lambda(property_name, property_range):
    print("generating number lambda")
    #notice if format is = vs (x-y) TODO
    return lambda host: True if int(host[property_name]) == int(property_range) else False


def gen_str_lambda(property_name, property_range):
    #TODO (low priority): implement regex
    return lambda host: False if host[property_name] is str(property_range) else True

#parse_component :: String -> Maybe([host -> Bool])
def parse_component(component_string):
    #split on equal
    split_str = component_string.split("=")
    if len(split_str) != 2:
        return None #this should probably be exceptions
    split_str = map(str.strip, split_str)
    property_name = split_str[0]
    property_range = split_str[1]
    #left is property
    if property_name not in test_host_model.keys():
        return None
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
    print(parse_querry("OS=Windows") (test_host_model))
    print(parse_querry("ports=80") (test_host_model))
    print(parse_querry("ports=ssh") (test_host_model))
    #print(parse_component("num_ports=3") (test_host_model))
