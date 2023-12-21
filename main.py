# main.py
from app.glacier_vaults_list import list_glacier_vaults
from app.list_archives import list_archives
from app.delete_archives import delete_archive
from app.delete_vault import delete_vault


def main():
    print("Retrieving list of AWS Glacier Vaults...")
    vault_names = list_glacier_vaults()

    print("Discovered Glacier Vaults:")
    for vault_name in vault_names:
        print(vault_name)

    print("\nProcessing each vault...")
    for vault_name in vault_names:
        print(f"Checking Vault: {vault_name}")

        # List archives in the vault
        archive_ids = list_archives(vault_name)

        # If the vault is empty, delete it
        if not archive_ids:
            print(f"Vault {vault_name} is empty. Deleting vault...")
            if delete_vault(vault_name):
                print(f"Vault {vault_name} deleted successfully.")
            else:
                print(f"Failed to delete vault {vault_name}.")
        else:
            # If the vault is not empty, delete each archive
            print("Discovered", len(archive_ids), "archives in vault",
                  vault_name)
            print("Deleting archives in vault", vault_name + "...")
            for archive_id in archive_ids:
                delete_archive(vault_name, archive_id)

            # After deleting all archives, delete the vault
            if delete_vault(vault_name):
                print("Vault", vault_name,
                      "deleted successfully after archive deletion.")
            else:
                print("Failed to delete vault", vault_name,
                      "after archive deletion.")


if __name__ == "__main__":
    main()
