#!/usr/bin/env python3
import yaml
import json
from jinja2 import Environment, FileSystemLoader
from collections.abc import Iterable, Hashable


def generate_terraform_file(config, template_env, output_file='main.tf'):
    def json_pretty_print(value):
        return json.dumps(value, indent=4, sort_keys=True)

    def comment_multiline(value):
        return '\n'.join([f'# {line}' for line in value.split('\n')])

    def pretty_format_yaml(input_data):
        if isinstance(input_data, str):
            try:
                data = yaml.safe_load(input_data)
            except Exception as e:
                raise ValueError(f"Error parsing YAML string: {e}")
        else:
            data = input_data

        try:
            return yaml.dump(data, default_flow_style=False, sort_keys=False, indent=2, allow_unicode=True)
        except Exception as e:
            raise ValueError(f"Error formatting YAML: {e}")

    with open(output_file, 'w') as file:
        # Getting the provider name to determine the template file name
        provider_name = config['virtual_machines_config']['global']['required_provider']

        if not isinstance(provider_name, str) or len(provider_name) == 0:
            raise Exception(f"Provider name {provider_name} is not recognized from virtual_machines_config.global.required_provider")
        
        template_file_name = f'vm_{provider_name}.j2'
        if not template_env.loader.get_source(template_env, template_file_name):
            raise Exception(f'Template file {template_file_name} does not exist')
        
        # Rendering the config into the template and writing to the output file
        template_env.filters['json_pretty_print'] = json_pretty_print
        template_env.filters['comment_multiline'] = comment_multiline
        template_env.filters['pretty_format_yaml'] = pretty_format_yaml
        rendered_config = template_env.get_template(template_file_name).render(config=config)
        file.write(rendered_config)


def main(config_path='config.yaml'):
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

    # Setting up the Jinja2 environment
    template_loader = FileSystemLoader(searchpath='./')
    template_env = Environment(loader=template_loader)

    # Generate the Terraform configuration file
    generate_terraform_file(config, template_env)


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    main(*args)
