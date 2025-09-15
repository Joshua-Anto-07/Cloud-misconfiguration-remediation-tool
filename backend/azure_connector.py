from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
import os

def get_resource_groups(subscription_id):
    credential = DefaultAzureCredential()
    client = ResourceManagementClient(credential, subscription_id)
    return [rg.name for rg in client.resource_groups.list()]

def get_storage_account_properties(subscription_id, resource_group_name, storage_account_name):
    credential = DefaultAzureCredential()
    storage_client = StorageManagementClient(credential, subscription_id)
    storage_account = storage_client.storage_accounts.get_properties(resource_group_name, storage_account_name)
    return {
        "location": storage_account.location,
        "account_tier": storage_account.sku.tier,
        "account_replication_type": storage_account.sku.name.replace('_', '').replace(storage_account.sku.tier, '')
    }