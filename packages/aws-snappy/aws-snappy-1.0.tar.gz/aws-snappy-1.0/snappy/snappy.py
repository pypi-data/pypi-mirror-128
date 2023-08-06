import boto3
import  snappy.utils.constants as Consts
from snappy.instance import Instance
from snappy.utils import helper as Helper

class Snappy():        
        
    def __init__(self, instances):

        # Create an empty list of instances
        self.instances = []

        # Create the boto3 EC2 client
        client = boto3.client('ec2')

        # Organize obtained instances into ip_addresses and hostnames
        ip_addresses, hostnames = Helper.organize_instances(instances)
        
        # Verify if IP addresses obtained
        if ip_addresses:
            
            # Get instance description from ip addresses
            response_ips = client.describe_instances(
                Filters=Consts.filter_boto3_template_ip(ip_addresses)
            )
            
            # Filter and append Instances from ip addresses
            for r in response_ips['Reservations']:
                for i in r['Instances']:
                    self.instances.append(Instance(i))
        
        # Verify if hostnames obtained
        if hostnames:  
            
            # Get instance description from hostname
            response_hostnames = client.describe_instances(
                Filters=Consts.filter_boto3_template_hostname(hostnames)
            )

            # Filter and append Instances from hostnames
            for r in response_hostnames['Reservations']:
                for i in r['Instances']:
                    self.instances.append(Instance(i))
        
        # Retrieve instances that were unable to fetch
        failed_instances = Helper.retrieve_failed_instances(instances, self.instances)
        
        # Check if there are failed instances
        if failed_instances:
            # Raise the exception
            raise Exception(Consts.EXCEPTION_MESSAGE_INSTANCES_RETRIEVAL_FAILED.format(str(failed_instances)))
        
        # Remove duplicate instances
        self.instances = Helper.remove_duplicate_instances(self.instances)
        
    def snap_roots(self, tags_specifications=None):
        # Make root snapshots for each instances and return the list of output
        return [instance.snap_root(tags_specifications) for instance in self.instances]