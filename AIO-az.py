# Import the needed credential and management objects from the libraries.
import os

from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient


print(
    "Provisioning virtual machines...some operations might take a \
minute or two."
)

# Acquire a credential object using CLI-based authentication.
credential = AzureCliCredential()

# Retrieve subscription ID from environment variable.
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]


# Obtain the management object for resources, using the credentials
# from the CLI login.
resource_client = ResourceManagementClient(credential, subscription_id)

RESOURCE_GROUP_NAME = "AIOAzure-VM-rg"
LOCATION = "westus2"

# Provision the resource group.
rg_result = resource_client.resource_groups.create_or_update(
    RESOURCE_GROUP_NAME, {"location": LOCATION}
)

print(
    f"Provisioned resource group {rg_result.name} in the \
{rg_result.location} region"
)


# Network and IP address names
VNET_NAME = "aio-example-vnet"
SUBNET1_NAME = "aio-example-subnet1"
SUBNET2_NAME = "aio-example-subnet2"
IP1_NAME = "aio-example-ip1"
IP2_NAME = "aio-example-ip2"
IP_CONFIG1_NAME = "aio-example-ip-config1"
IP_CONFIG2_NAME = "aio-example-ip-config2"
NIC1_NAME = "aio-example-nic1"
NIC2_NAME = "aio-example-nic2"
STORAGE_ACCOUNT_NAME = "aio-examplestorage"

# Obtain the management object for networks
network_client = NetworkManagementClient(credential, subscription_id)

# Provision the virtual network and wait for completion
poller = network_client.virtual_networks.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    VNET_NAME,
    {
        "location": LOCATION,
        "address_space": {"address_prefixes": ["10.0.0.0/16"]},
    },
)

vnet_result = poller.result()

print(
    f"Provisioned virtual network {vnet_result.name} with address \
prefixes {vnet_result.address_space.address_prefixes}"
)

# Step 3: Provision subnet1 and wait for completion
poller = network_client.subnets.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    VNET_NAME,
    SUBNET1_NAME,
    {"address_prefix": "10.0.0.0/24"},
)
subnet1_result = poller.result()

print(
    f"Provisioned virtual subnet {subnet1_result.name} with address \
prefix {subnet1_result.address_prefix}"
)

# Step 4: Provision subnet2 and wait for completion
poller = network_client.subnets.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    VNET_NAME,
    SUBNET2_NAME,
    {"address_prefix": "10.0.1.0/24"},
)
subnet2_result = poller.result()

print(
    f"Provisioned virtual subnet {subnet2_result.name} with address \
prefix {subnet2_result.address_prefix}"
)

# Step 5: Provision IP1 address and wait for completion
poller = network_client.public_ip_addresses.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    IP1_NAME,
    {
        "location": LOCATION,
        "sku": {"name": "Standard"},
        "public_ip_allocation_method": "Static",
        "public_ip_address_version": "IPV4",
    },
)

ip1_address_result = poller.result()

print(
    f"Provisioned public IP address {ip1_address_result.name} \
with address {ip1_address_result.ip_address}"
)

# Step 6: Provision IP2 address and wait for completion
poller = network_client.public_ip_addresses.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    IP2_NAME,
    {
        "location": LOCATION,
        "sku": {"name": "Standard"},
        "public_ip_allocation_method": "Static",
        "public_ip_address_version": "IPV4",
    },
)

ip2_address_result = poller.result()

print(
    f"Provisioned public IP address {ip2_address_result.name} \
with address {ip2_address_result.ip_address}"
)

# Step 7: Provision NIC1
poller = network_client.network_interfaces.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    NIC1_NAME,
    {
        "location": LOCATION,
        "ip_configurations": [
            {
                "name": IP_CONFIG1_NAME,
                "subnet": {"id": subnet1_result.id},
                "public_ip_address": {"id": ip1_address_result.id},
            }
        ],
    },
)

nic1_result = poller.result()

print(f"Provisioned network interface client {nic1_result.name}")

# Step 8: Provision NIC2
poller = network_client.network_interfaces.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    NIC2_NAME,
    {
        "location": LOCATION,
        "ip_configurations": [
            {
                "name": IP_CONFIG2_NAME,
                "subnet": {"id": subnet2_result.id},
                "public_ip_address": {"id": ip2_address_result.id},
            }
        ],
    },
)

nic2_result = poller.result()

print(f"Provisioned network interface client {nic2_result.name}")

# Management object for virtual machines
compute_client = ComputeManagementClient(credential, subscription_id)

VM1_NAME = "AIOvm1"
USERNAME = "aiouser1"
PASSWORD = "ChangePa$$w0rd1"

print(
    f"Provisioning virtual machine {VM1_NAME}; this operation might \
take a few minutes."
)


poller = compute_client.virtual_machines.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    VM1_NAME,
    {
        "location": LOCATION,
        "storage_profile": {
            "image_reference": {
                "publisher": "Canonical",
                "offer": "UbuntuServer",
                "sku": "22.04.2-LTS",
                "version": "latest",
            }
        },
        "hardware_profile": {"vm_size": "Standard_DS1_v2"},
        "os_profile": {
            "computer_name": VM1_NAME,
            "admin_username": USERNAME,
            "admin_password": PASSWORD,
        },
        "network_profile": {
            "network_interfaces": [
                {
                    "id": nic1_result.id,
                }
            ]
        },
    },
)

vm1_result = poller.result()

print(f"Provisioned virtual machine {vm1_result.name}")

VM2_NAME = "AIOvm2"
USERNAME = "aiouser2"
PASSWORD = "ChangePa$$w0rd2"

print(
    f"Provisioning virtual machine {VM2_NAME}; this operation might \
take a few minutes."
)

# Provision VM2 and a default virtual network/subnet.

poller = compute_client.virtual_machines.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    VM2_NAME,
    {
        "location": LOCATION,
        "storage_profile": {
            "image_reference": {
                "publisher": "Canonical",
                "offer": "UbuntuServer",
                "sku": "22.04.2-LTS",
                "version": "latest",
            }
        },
        "hardware_profile": {"vm_size": "Standard_DS1_v2"},
        "os_profile": {
            "computer_name": VM2_NAME,
            "admin_username": USERNAME,
            "admin_password": PASSWORD,
        },
        "network_profile": {
            "network_interfaces": [
                {
                    "id": nic2_result.id,
                }
            ]
        },
    },
)

vm2_result = poller.result()

print(f"Provisioned virtual machine {vm2_result.name}")
