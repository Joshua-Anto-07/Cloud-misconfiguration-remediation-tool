import yaml
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from .azure_connector import get_resource_groups

SUBSCRIPTION_ID = "8bbab1a3-5bc8-408e-ba14-568523743538"  # Replace with your actual subscription ID

def load_rules():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)['rules']

def compare_values(actual, expected):
    """Recursively compare actual values to expected values (supports dicts, lists, scalars)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(compare_values(actual.get(k), v) for k, v in expected.items())
    elif isinstance(expected, list):
        return isinstance(actual, list) and all(item in actual for item in expected)
    else:
        return actual == expected

def get_nested_property(obj, prop_path):
    """Dynamically fetch a nested property from an object using dot notation (e.g., 'network_rule_set.default_action')."""
    if not prop_path:
        return obj
    current = obj
    for part in prop_path.split('.'):
        if current is None:
            return None
        current = getattr(current, part, None)
    return current

def evaluate_property(account, fetch_config):
    """Evaluate a property based on its fetch_config (only nested type)."""
    try:
        if fetch_config['type'] == 'nested':
            # Try fetching from account directly, then from properties
            value = get_nested_property(account, fetch_config.get('path'))
            if value is None and hasattr(account, 'properties'):
                value = get_nested_property(account.properties, fetch_config.get('path'))
            return value
    except Exception as e:
        print(f"Error evaluating fetch_config {fetch_config}: {e}")
        return None
    return None

def run_benchmarks():
    rules = load_rules()
    results = []
    credential = DefaultAzureCredential()
    storage_client = StorageManagementClient(credential, SUBSCRIPTION_ID)
    resource_groups = get_resource_groups(SUBSCRIPTION_ID)

    for rule in rules:
        if rule['resource_type'] == 'storage_account':
            for rg in resource_groups:
                print(f"Checking resource group: {rg} for rule: {rule['id']}")
                storage_accounts = storage_client.storage_accounts.list_by_resource_group(rg)
                for account in storage_accounts:
                    for prop, config in rule['properties'].items():
                        actual = evaluate_property(account, config['fetch_config'])
                        status = "pass" if compare_values(actual, config['expected']) else "fail"
                        
                        results.append({
                            "check_id": rule['id'],
                            "description": rule['description'],
                            "status": status,
                            "resource_group": rg,
                            "storage_account": account.name,
                            "property": prop,
                            "actual": actual,
                            "expected": config['expected'],
                            "remediation": rule['remediation']
                        })
    return results