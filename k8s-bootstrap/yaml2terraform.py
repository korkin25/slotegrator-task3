import yaml
from jinja2 import Environment, FileSystemLoader
import pprint


def generate_terraform_file(config, template_env, output_file='main.tf'):
    with open(output_file, 'w') as file:
        # Get the SSH key path
        ssh_key = config.get('ssh_key', '')

        # Process provider information
        vm_global_config = config['virtual_machines_config']['global']
        vm_providers_info = vm_global_config['required_providers']
        vm_provider_config = template_env.get_template('provider_template.j2').render(providers=vm_providers_info)
        file.write(vm_provider_config)

        # Generate VM configurations
        vms_config = config['virtual_machines_config']['virtual_machines']
        for vm in vms_config:
            for vm_type in vm.keys():
                print(f"Generating configuration for VM type: {vm_type}:\n")
                pprint.pprint(vm_type)

                for i in range(vm_type.counts):
                    vm_name = f"{vm.get('name', vm_type)}-{i}"
                    terraform_config = template_env.get_template('vm_template.j2').render(
                        vm=vm, vm_name=vm_name, ssh_key=ssh_key
                    )
                    file.write(terraform_config)

        # Add output blocks
        output_config = template_env.get_template('output_template.j2').render(vms=vms_config)
        file.write(output_config)


def main(config_path='config.yaml'):
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Configuration file {config_path} not found.")
        return
    except Exception as e:
        print(f"Error opening configuration file: {str(e)}")
        return

    template_loader = FileSystemLoader(searchpath='./')
    template_env = Environment(loader=template_loader)

    generate_terraform_file(config, template_env)


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    main(*args)
