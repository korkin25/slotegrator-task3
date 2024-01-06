#!/usr/bin/env python3
import yaml
from jinja2 import Environment, FileSystemLoader
import pprint

def generate_terraform_file(config, template_env, output_file='main.tf'):
    with open(output_file, 'w') as file:
        # Determine the template file name based on the provider name
        provider_name = config['virtual_machines_config']['global']['required_provider']
        template_file_name = f'vm_{provider_name}.j2'

        # Render the template with the entire config
        rendered_config = template_env.get_template(template_file_name).render(config=config)
        file.write(rendered_config)

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

    print("Configuration file:")
    pprint.pprint(config)

    template_loader = FileSystemLoader(searchpath='./')
    template_env = Environment(loader=template_loader)

    generate_terraform_file(config, template_env)

if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    main(*args)
