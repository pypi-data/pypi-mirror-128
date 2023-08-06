import re

from datetime import date

def format_today():
    # This function returns today's date
    # in the following format YYYYMMDD
    today = date.today()
    return today.strftime("%Y%m%d")

def retrieve_failed_instances(previous_instances, retrieved_instances):
    
    # Definition of failed instances
    failed_instances = []
    
    # Organize previous instances
    previous_ip_addresses, previous_hostnames = organize_instances(previous_instances)
    
    # Get retrieved instances
    retrieved_ip_addresses = [instance.private_ip for instance in retrieved_instances]
    retrieved_hostnames = [instance.name for instance in retrieved_instances]
    
    failed_instances = failed_instances + [instance for instance in previous_ip_addresses if (instance not in retrieved_ip_addresses and instance not in retrieved_hostnames)]
    failed_instances = failed_instances + [instance for instance in previous_hostnames if (instance not in retrieved_ip_addresses and instance not in retrieved_hostnames)]
    
    return failed_instances

def is_an_ip_address(data):
    # Checks whether a given string
    # has ip address format
    pat = re.match("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", data)
    return bool(pat)

def organize_instances(instances_raw):
    # Return ip_addresses, hostnames
    return [ip for ip in instances_raw if is_an_ip_address(ip)], [hostname for hostname in instances_raw if not is_an_ip_address(hostname)]

def remove_duplicate_instances(instances):
    
    # Remove duplicates in list of instances
    new_list = []
    
    for instance in instances:
        
        is_present = any(x.private_ip == instance.private_ip for x in new_list)

        if not is_present:
            new_list.append(instance)
    
    return new_list