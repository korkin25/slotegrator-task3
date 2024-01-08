#!/bin/sh

#export TF_LOG=INFO

if ! python3 yaml2terraform.py; then
    echo "Error: yaml2terraform.py failed"
    exit 1
fi

if ! terraform init; then
    echo "Error: terraform init failed"
    exit 1
fi

if ! terraform validate; then
    echo "Error: terraform validate failed"
    exit 1
fi

terraform refresh 
terraform plan
terraform apply -auto-approve 

./tfstate_get_network.py

