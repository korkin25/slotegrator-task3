import yaml
import json

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_terraform_input(yaml_data):
    vm_data = yaml_data.get("virtual_machines", [])
    k8s_config = yaml_data.get("kubernetes_config", {})

    # Генерация данных для VirtualBox провайдера
    vbox_data = [
        {
            "name": vm["name"],
            "cpu": vm["cpu"],
            "memory": vm["memory"],
            "disk_size": vm["disk_size"]
        }
        for vm in vm_data
    ]

    # Генерация данных для k0s провайдера
    k0s_data = {
        "version": k8s_config.get("version"),
        "network_plugin": k8s_config.get("network_plugin"),
        "nodes": [
            {
                "name": vm["name"],
                "role": vm["role"]
            }
            for vm in vm_data
        ]
    }

    return {"virtualbox": vbox_data, "k0s": k0s_data}

def main():
    config_path = 'config.yaml'
    yaml_data = read_yaml(config_path)
    terraform_input = generate_terraform_input(yaml_data)

    print(json.dumps(terraform_input, indent=4))

if __name__ == "__main__":
    main()
