

import toml


def get_conf(conf_file):
    """   """    
    
    with open(conf_file,'r') as conf_h:
        
        conf = toml.loads(conf_h.read())
    
    return conf