#!/bin/sh

. ./.env

env | grep GITHUB
ansible-galaxy install monolithprojects.github_actions_runner
ansible-playbook -i inventory.yml playbook.yml "$@"
