from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials

# Get the compute service
credentials = GoogleCredentials.get_application_default()
compute = discovery.build('compute', 'v1', credentials=credentials)

# Project and region parameters
project = 'AIO_project'
region = 'us-central1'

# Create the VPC
network_body = {'name': 'AIO-network'}
network = compute.networks().insert(project=project, body=network_body).execute()

# Create the subnet
subnet_body = {'name': 'AIO-subnet', 'ipCidrRange': '10.0.0.0/16', 'network': network['selfLink']}
subnet = compute.subnetworks().insert(project=project, region=region, body=subnet_body).execute()

# Function to create the VM with a network interface
def create_instance(name):
    instance_body = {
        'name': name,
        'disks': [
            {
                'boot': True,
                'autoDelete': False,
                'initializeParams': {
                    'sourceImage': 'projects/debian-cloud/global/images/family/debian-9',
                    'diskSizeGb': '10',
                },
            },
        ],
        'networkInterfaces': [
            {'network': network['selfLink'], 'subnetwork': subnet['selfLink']},
        ],
    }
    yield compute.instances().insert(project=project, zone='us-central1-a', body=instance_body).execute()

# Create the two VM instances
instance1 = create_instance('AIO-instance-1')
instance2 = create_instance('AIO-instance-2')
