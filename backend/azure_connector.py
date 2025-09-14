from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

def get_resource_groups(subscription_id):
    credential = DefaultAzureCredential()
    client = ResourceManagementClient(credential, subscription_id)
    return [rg.name for rg in client.resource_groups.list()]
