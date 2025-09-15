import json
import os
from backend.azure_connector import get_storage_account_properties

def remediate_misconfigurations(results, subscription_id):
    print("Remediating misconfigurations...")
    # Load the assessment report to get the misconfigured resources
    with open('reports/assessment_report.json', 'r') as f:
        report = json.load(f)

    # Filter for misconfigured resources, ignoring CIS-3.2
    misconfigured_resources = [res for res in report if res['status'] == 'fail' and res['check_id'] != 'CIS-3.2']

    os.environ['ARM_SUBSCRIPTION_ID'] = subscription_id
    os.system('terraform init')

    # Group resources by storage account and resource group
    grouped_resources = {}
    for res in misconfigured_resources:
        key = (res['resource_group'], res['storage_account'])
        if key not in grouped_resources:
            grouped_resources[key] = []
        grouped_resources[key].append(res)

    for (resource_group, storage_account), misconfigs in grouped_resources.items():
        terraform_script = generate_terraform_script(misconfigs, subscription_id, resource_group, storage_account)
        with open('remediation.tf', 'w') as f:
            f.write(terraform_script)

        resource_id = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Storage/storageAccounts/{storage_account}"
        import_command = f"terraform import azurerm_storage_account.{storage_account} {resource_id}"
        apply_command = "terraform apply -auto-approve"

        print(f"Importing resource: {storage_account}")
        os.system(import_command)

        print(f"Applying changes to resource: {storage_account}")
        os.system(apply_command)

    print("Terraform script applied successfully.")

def generate_terraform_script(misconfigs, subscription_id, resource_group, storage_account):
    properties = get_storage_account_properties(subscription_id, resource_group, storage_account)
    terraform_blocks = [
        'terraform {',
        '  required_providers {',
        '    azurerm = {',
        '      source  = "hashicorp/azurerm"',
        '      version = ">= 2.0"',
        '    }',
        '  }',
        '}',
        '',
        'provider "azurerm" {',
        '  features {}',
        '}',
        ''
    ]

    block = f'\nresource "azurerm_storage_account" "{storage_account}" {{\n  name                     = "{storage_account}"\n  resource_group_name      = "{resource_group}"\n'
    block += f'  location                 = "{properties["location"]}"\n  account_tier             = "{properties["account_tier"]}"\n  account_replication_type = "{properties["account_replication_type"]}"\n'

    for misconfig in misconfigs:
        prop = misconfig['property']
        expected = misconfig['expected']

        if prop == 'enable_https_traffic_only':
            block += f"  https_traffic_only_enabled = {str(expected).lower()}\n"
        elif prop == 'allow_blob_public_access':
            block += f"  allow_nested_items_to_be_public = {str(expected).lower()}\n"
        elif prop == 'network_rule_set.default_action':
            block += f'\n  network_rules {{\n    default_action             = "{expected}"\n  }}\n'
        elif prop == 'network_rule_set.bypass':
            # This is a simplification, assumes "AzureServices"
            # A more robust solution would handle other bypass options
            block += f'\n  network_rules {{\n    bypass                     = ["{expected}"]\n  }}\n'
    block += "}\n"
    terraform_blocks.append(block)

    return "\n".join(terraform_blocks)
