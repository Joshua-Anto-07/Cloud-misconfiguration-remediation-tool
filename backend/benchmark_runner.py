from azure_connector import get_resource_groups
from report_generator import save_report
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient

SUBSCRIPTION_ID = "8bbab1a3-5bc8-408e-ba14-568523743538"  # Replace this with your actual subscription ID

def check_public_storage_access(subscription_id):
    credential = DefaultAzureCredential()
    storage_client = StorageManagementClient(credential, subscription_id)

    results = []
    resource_groups = get_resource_groups(subscription_id)

    for rg in resource_groups:
        print(f"Checking resource group: {rg}")
        try:
            storage_accounts = storage_client.storage_accounts.list_by_resource_group(rg)
        except Exception as e:
            print(f"Error listing storage accounts in {rg}: {e}")
            continue

        for account in storage_accounts:
            name = account.name
            print(f"  - Checking storage account: {name}")

            try:
                allow_public_access = account.allow_blob_public_access

                if allow_public_access is False:
                    status = "pass"
                elif allow_public_access is True:
                    status = "fail"
                else:
                    status = "unknown"
            except Exception as e:
                print(f"    Error retrieving access info for {name}: {e}")
                status = "unknown"

            results.append({
                "check_id": "CIS-1.1",
                "description": "Ensure no Storage Account allows public access",
                "status": status,
                "resource_group": rg,
                "storage_account": name,
                "remediation": "Set `allow_blob_public_access` to false on the storage account"
            })

    return results


if __name__ == "__main__":
    print("🔍 Running public access check on storage accounts...")
    results = check_public_storage_access(SUBSCRIPTION_ID)
    save_report(results)
    print("✅ Done. Results saved in reports/assessment_report.json")
