#!/usr/bin/env python3
import json
import subprocess

def get_terraform_state():
    """Get the Terraform state file in JSON format."""
    result = subprocess.run(["terraform", "show", "-json"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("Error getting Terraform state: " + result.stderr)
    return json.loads(result.stdout)

def extract_provider_info(state):
    """Extract provider information from the Terraform state."""
    resources = state.get("values", {}).get("root_module", {}).get("resources", [])
    if not resources:
        raise Exception("No resources found in Terraform state")

    # Find the first resource and use its provider
    first_resource = resources[0]
    provider_name = first_resource.get("provider_name", "").split("/")[1]  # Example: 'registry.terraform.io/terraform-lxd/lxd' -> 'lxd'
    if not provider_name:
        raise Exception("No provider information found in the first resource of Terraform state")

    return provider_name


def extract_vm_info(state, provider_name):
    """Extract VM information based on the provider from the Terraform state."""
    # Define the mapping of provider to its hostname and IP keys
    key_mappings = {
        "terraform-lxd": {"hostname": "name", "ip_address": "ipv4_address"},
        # Add other providers and their respective keys here
    }

    if provider_name not in key_mappings:
        raise Exception(f"No key mapping defined for provider: {provider_name}")

    keys = key_mappings[provider_name]
    hosts_entries = []
    for resource in state.get("values", {}).get("root_module", {}).get("resources", []):
        if resource.get("type") == "lxd_instance":  # Adjust according to provider
            attributes = resource.get("values")
            hostname = attributes.get(keys["hostname"])
            ip_address = attributes.get(keys["ip_address"])
            if ip_address and hostname:
                hosts_entries.append(f"{ip_address} {hostname}")
    return hosts_entries



def main():
    state = get_terraform_state()
    provider_name = extract_provider_info(state)
    hosts_entries = extract_vm_info(state, provider_name)
    for entry in hosts_entries:
        print(entry)

if __name__ == "__main__":
    main()

