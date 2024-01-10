#!/bin/sh

export TF_LOG=DEBUG

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
if ! terraform apply -auto-approve; then
    echo "Error: terraform apply failed"
    exit 1
fi


